## Python 垃圾回收机制

Python的垃圾回收机制包括了两大部分：

- **引用计数**(大部分在 `Include/object.h` 中定义)
- **标记清除+隔代回收**(大部分在 `Modules/gcmodule.c` 中定义)



## 1. 引用计数机制

python中万物皆对象，他的核心结构是：`PyObject`

```c++
typedef __int64 ssize_t;

typedef ssize_t         Py_ssize_t;

typedef struct _object {
    _PyObject_HEAD_EXTRA
    Py_ssize_t ob_refcnt;   // Py_ssize_t __int64
    struct _typeobject *ob_type;
} PyObject;

typedef struct {
    PyObject ob_base;
    Py_ssize_t ob_size; /* Number of items in variable part */
} PyVarObject;
```

`PyObject`是每个对象的底层数据结构，其中`ob_refcnt`就是作为引用计数。当一个对象有新的引用时, 它的`ob_refcnt`就会增加，当引用它的对象被删除，它的`ob_refcnt`就会减少,当引用技术为0时，该对象的生命结束了。

1. 引用计数+1的情况
   - 对象被创建 eg: a=2
   - 对象被引用 eg: b=a
   - 对象被作为参数，传入到一个函数中，例如func(a)
   - 对象作为一个元素，存储在容器中，例如list1=[a, b]
2. 引用计数-1的情况
   - 对象的别名被显示的销毁 eg: del a
   - 对象的别名被赋予新的对象  eg: a=34
   - 一个对象离开它的作用域， 例如f函数执行完毕时，func函数中的局部变量（全局变量不会）
   - 对象所在的容器被销毁，或者从容器中删除

**如何查看对象的引用计数**

```python
import sys
a = 'hello'
sys.getrefcount(a)   
// 注意: getrefcount(a) 传入a时, a的引用计数会加1
```

### 1.1 什么时候触发回收

当一个对象的引用计数变为了 0, 会直接进入释放空间的流程

```c++
/* cpython/Include/object.h */
static inline void _Py_DECREF(const char *filename, int lineno,
                              PyObject *op)
{
    _Py_DEC_REFTOTAL;
    if (--op->ob_refcnt != 0) {
#ifdef Py_REF_DEBUG
        if (op->ob_refcnt < 0) {
            _Py_NegativeRefcount(filename, lineno, op);
        }
#endif
    }
    else {
    	/* // _Py_Dealloc 会找到对应类型的 descructor, 并且调用这个 descructor
        destructor dealloc = Py_TYPE(op)->tp_dealloc;
        (*dealloc)(op);
        */
        _Py_Dealloc(op);
    }
}
```

## 2. 常驻内存对象

引用计数机制所带来的维护引用计数的额外操作，与python运行中所进行的内存分配、释放、引用赋值的次数是成正比的，这一点，相对于主流的垃圾回收技术，比如标记--清除`(mark--sweep)`、停止--复制`(stop--copy)`等方法相比是一个弱点，因为它们带来额外操作只和内存数量有关，至于多少人引用了这块内存则不关心。因此为了与引用计数搭配、在内存的分配和释放上获得最高的效率，python设计了大量的内存池机制，比如**小整数对象池、字符串的intern机制，列表的freelist缓冲池**等等，这些大量使用的面向特定对象的内存池机制正是为了弥补引用计数的软肋。

### 2.1 小整数对象池

```c++
#ifndef NSMALLPOSINTS
#define NSMALLPOSINTS           257
#endif
#ifndef NSMALLNEGINTS
#define NSMALLNEGINTS           5
#endif

#if NSMALLNEGINTS + NSMALLPOSINTS > 0
/* Small integers are preallocated in this array so that they
   can be shared.
   The integers that are preallocated are those in the range
   -NSMALLNEGINTS (inclusive) to NSMALLPOSINTS (not inclusive).
*/
static PyLongObject small_ints[NSMALLNEGINTS + NSMALLPOSINTS];

Py_INCREF(op)  增加对象引用计数

Py_DECREF(op)  减少对象引用计数, 如果计数位0, 调用_Py_Dealloc

_Py_Dealloc(op) 调用对应类型的 tp_dealloc 方法
```

小整数对象池就是一个`PyLongObject` 数组, 大小=257+5=262, 范围是`[-5, 257)` 注意左闭右开. 

> python对小整数的定义是[-5, 257)， 这些整数对象是提前建立好的，不会被垃圾回收，在一个python程序中，所有位于这个范围内的整数使用的都是同一个对象
>

### 2.2 大整数对象池

疑惑：《Python源码剖析》提到的整数对象池block_list应该已经不存在了（因为PyLongObject为变长对象）。`Python2`中的`PyIntObject`实际是对`c`中的`long`的包装。所以`Python2`也提供了专门的缓存池，供大整数轮流使用，避免每次使用不断的`malloc`分配内存带来的效率损耗，可参考[刘志军老师的讲解](https://foofish.net/python_int_implement.html)。既然没有池了，malloc/free会带来的不小性能损耗。Guido认为Py3.0有极大的优化空间，在字符串和整形操作上可以取得很好的优化结果。

```c
/* Allocate a new int object with size digits.
   Return NULL and set exception if we run out of memory. */

#define MAX_LONG_DIGITS \
    ((PY_SSIZE_T_MAX - offsetof(PyLongObject, ob_digit))/sizeof(digit))

PyLongObject *
_PyLong_New(Py_ssize_t size)
{
    PyLongObject *result;
    /* Number of bytes needed is: offsetof(PyLongObject, ob_digit) +
       sizeof(digit)*size.  Previous incarnations of this code used
       sizeof(PyVarObject) instead of the offsetof, but this risks being
       incorrect in the presence of padding between the PyVarObject header
       and the digits. */
    if (size > (Py_ssize_t)MAX_LONG_DIGITS) {
        PyErr_SetString(PyExc_OverflowError,
                        "too many digits in integer");
        return NULL;
    }
    result = PyObject_MALLOC(offsetof(PyLongObject, ob_digit) +
                             size*sizeof(digit));
    if (!result) {
        PyErr_NoMemory();
        return NULL;
    }
    return (PyLongObject*)PyObject_INIT_VAR(result, &PyLong_Type, size);
}
```

> `result = PyObject_MALLOC(offsetof(PyLongObject, ob_digit) +  size*sizeof(digit));`

每一个大整数，均创建一个新的对象。id(num)均不同。

### 2.4 字符串的intern机制

> ```
> Objects/unicodeobject.c
> Objects/codeobject.c
> ```

> `PyStringObject`对象的intern机制之目的是：对于被intern之后的字符串，比如“Ruby”，在整个Python的运行期间，系统中都只有唯一的一个与字符串“Ruby”对应的`PyStringObject`对象。这样当判断两个`PyStringObject`对象是否相同时，如果它们都被intern了，那么只需要简单地检查它们对应的`PyObject*`是否相同即可。这个机制既节省了空间，又简化了对`PyStringObject`对象的比较，嗯，可谓是一箭双雕哇。
>
> 摘自：《Python源码剖析》 — 陈儒

Python3中`PyUnicodeObject`对象的`intern`机制和Python2的`PyStringObject`对象`intern`机制一样，主要为了节省内存的开销，利用字符串对象的不可变性，对存在的字符串对象重复利用

```powershell
In [50]: a = 'python'

In [51]: b = 'python'

In [52]: id(a)
Out[52]: 442782398256

In [53]: id(b)
Out[53]: 442782398256

In [54]: b = 'hello python'

In [55]: a = 'hello python'

In [56]: id(a)
Out[56]: 442808585520

In [57]: id(b)
Out[57]: 442726541488
```

**什么样的字符串会使用`intern`机制?**

intern机制跟编译时期有关，相关代码在`Objects/codeobject.c`

```c++
/* Intern selected string constants */
static int
intern_string_constants(PyObject *tuple)
{
    int modified = 0;
    Py_ssize_t i;

    for (i = PyTuple_GET_SIZE(tuple); --i >= 0; ) {
        PyObject *v = PyTuple_GET_ITEM(tuple, i);
        if (PyUnicode_CheckExact(v)) {
            if (PyUnicode_READY(v) == -1) {
                PyErr_Clear();
                continue;
            }
            if (all_name_chars(v)) {
                PyObject *w = v;
                PyUnicode_InternInPlace(&v);
                if (w != v) {
                    PyTuple_SET_ITEM(tuple, i, v);
                    modified = 1;
                }
            }
        }
        /*....*/
}
    
/* all_name_chars(s): true iff s matches [a-zA-Z0-9_]* */
static int
all_name_chars(PyObject *o)
{
    const unsigned char *s, *e;

    if (!PyUnicode_IS_ASCII(o))
        return 0;

    s = PyUnicode_1BYTE_DATA(o);
    e = s + PyUnicode_GET_LENGTH(o);
    for (; s != e; s++) {
        if (!Py_ISALNUM(*s) && *s != '_')
            return 0;
    }
    return 1;
}

```

> 可见 all_name_chars 决定了是否会 intern，简单来说就是 ascii 字母，数字和下划线组成的字符串会被缓存。但是不仅如此。2.5还会说

```c++
/* This dictionary holds all interned unicode strings.  Note that references
   to strings in this dictionary are *not* counted in the string's ob_refcnt.
   When the interned string reaches a refcnt of 0 the string deallocation
   function will delete the reference from this dictionary.

   Another way to look at this is that to say that the actual reference
   count of a string is:  s->ob_refcnt + (s->state ? 2 : 0)
*/
static PyObject *interned = NULL;
/*省略*/
void
PyUnicode_InternInPlace(PyObject **p)
{
    PyObject *s = *p;
    PyObject *t;
#ifdef Py_DEBUG
    assert(s != NULL);
    assert(_PyUnicode_CHECK(s));
#else
    if (s == NULL || !PyUnicode_Check(s))
        return;
#endif
    /* If it's a subclass, we don't really know what putting
       it in the interned dict might do. */
    if (!PyUnicode_CheckExact(s))
        return;
    // [1]
    if (PyUnicode_CHECK_INTERNED(s))
        return;
    if (interned == NULL) {
        interned = PyDict_New();
        if (interned == NULL) {
            PyErr_Clear(); /* Don't leave an exception */
            return;
        }
    }
    Py_ALLOW_RECURSION
    // [2]
    t = PyDict_SetDefault(interned, s, s);
    Py_END_ALLOW_RECURSION
    if (t == NULL) {
        PyErr_Clear();
        return;
    }
    // [3]
    if (t != s) {
        Py_INCREF(t);
        Py_SETREF(*p, t);
        return;
    }
    // [4]
    /* The two references in interned are not counted by refcnt.
       The deallocator will take care of this */
    Py_REFCNT(s) -= 2;
    _PyUnicode_STATE(s).interned = SSTATE_INTERNED_MORTAL;
}
```

通过函数我们可以得知，python中维护这一个interned变量的指针，这个变量指向`PyDict_New`创建的对象，而`PyDict_New`实际上创建了一个`PyDictObject`对象，是Python中`dict`类型的对象。实际上intern机制就是维护一个字典，这个字典中记录着被intern机制处理过的字符串对象，`[1]`处`PyUnicode_CHECK_INTERNED`宏检查字符串对象的`state.interned`是否被标记，

如果字符串对象的`state.interned`被标记了，就直接返回；`[2]`处**尝试**把没有被标记的`字符串对象s`作为`key-value`加入`interned`字典中；`[3]`处表示`字符串对象s`已经在`interned`字典中（对应的value值是`字符串对象t`），（通过`Py_SETREF`宏来改变p指针的指向），且原`字符串对象p`会因引用计数为零被回收。`Py_SETREF`宏在`Include/object.h`定义着：

```c
/* Safely decref `op` and set `op` to `op2`.
 *
 * As in case of Py_CLEAR "the obvious" code can be deadly:
 *
 *     Py_DECREF(op);
 *     op = op2;
 *
 * The safe way is:
 *
 *      Py_SETREF(op, op2);
 *
 * That arranges to set `op` to `op2` _before_ decref'ing, so that any code
 * triggered as a side-effect of `op` getting torn down no longer believes
 * `op` points to a valid object.
 *
 * Py_XSETREF is a variant of Py_SETREF that uses Py_XDECREF instead of
 * Py_DECREF.
 */

#define Py_SETREF(op, op2)                      \
    do {                                        \
        PyObject *_py_tmp = (PyObject *)(op);   \
        (op) = (op2);                           \
        Py_DECREF(_py_tmp);                     \
    } while (0)
```

`[4]`中把新加入`interned`字典中的字符串对象做减引用操作，并把`state.interned`标记成`SSTATE_INTERNED_MORTAL`。`SSTATE_INTERNED_MORTAL`表示字符串对象被intern机制处理，但会随着引用计数被回收；`interned`标记还有另外一种`SSTATE_INTERNED_IMMORTAL`，表示被intern机制处理但对象不可销毁，会与Python解释器同在。`PyUnicode_InternInPlace`只能创建`SSTATE_INTERNED_MORTAL`状态的字符串，要想创建`SSTATE_INTERNED_IMMORTAL`状态的字符串需要通过另外一个接口，强制改变intern的状态

```c++
void
PyUnicode_InternImmortal(PyObject **p)
{
    PyUnicode_InternInPlace(p);
    if (PyUnicode_CHECK_INTERNED(*p) != SSTATE_INTERNED_IMMORTAL) {
        _PyUnicode_STATE(*p).interned = SSTATE_INTERNED_IMMORTAL;
        Py_INCREF(*p);
    }
}
```



**为什么引用`Py_REFCNT(s) -= 2;`要-2呢？**



```c++
PyDict_SetDefault(PyObject *d, PyObject *key, PyObject *defaultobj)
{
    PyDictObject *mp = (PyDictObject *)d;
    PyObject *value;
    Py_hash_t hash;

    /*...*/
    if (ix == DKIX_EMPTY) {
        /*...*/
        Py_ssize_t hashpos = find_empty_slot(mp->ma_keys, hash);
        ep0 = DK_ENTRIES(mp->ma_keys);
        ep = &ep0[mp->ma_keys->dk_nentries];
        dictkeys_set_index(mp->ma_keys, hashpos, mp->ma_keys->dk_nentries);
        Py_INCREF(key);
        Py_INCREF(value);
        /*...*/
    return value;
}
```

> 对于被intern机制处理了的PyStringObject对象，Python采用了特殊的引用计数机制。在将一个PyStringObject对象a的PyObject指针**作为key和value**添加到interned中时，PyDictObject对象会通过这两个指针对a的引用计数进行两次加1的操作。但是Python的设计者规定在interned中a的指针不能被视为对象a的有效引用，因为如果是有效引用的话，那么a的引用计数在Python结束之前永远都不可能为0，因为interned中至少有两个指针引用了a，那么删除a就永远不可能了，这显然是没有道理的。
> 摘自：《Python源码剖析》 — 陈儒



**注意：**实际上，即使Python会对一个字符串进行intern机制的处理，也会先创建一个`PyUnicodeObject`对象，然后检查在`interned`字典中是否有值和其相同，存在的话就将`interned`字典保存的value值返回，之前临时创建的字符串对象会由于引用计数为零而回收。

**是否可以直接对C原生对象做intern的动作呢？不需要创建临时对象**

事实上`CPython`确实提供了以`char * `为参数的intern机制相关函数，但是，也是一样的创建temp在设置intern.

```c++
PyUnicode_InternImmortal(PyObject **p)
{
    PyUnicode_InternInPlace(p);
    if (PyUnicode_CHECK_INTERNED(*p) != SSTATE_INTERNED_IMMORTAL) {
        _PyUnicode_STATE(*p).interned = SSTATE_INTERNED_IMMORTAL;
        Py_INCREF(*p);
    }
}
```

**为什么需要临时对象？**

> 因为PyDict_SetDefault() 操作的是PyDictObject对象，而该对象必须以PyObject*指针作为键

### 2.5 字符缓冲池（单字符）

python为小整数对象准备了小整数对象池，当然对于常用的字符，python对应的也建了字符串缓冲池，因为 python3 中通过 `unicode_latin1[256] `**将长度为 1 的 ascii 的字符也缓存了**

```c
/* Single character Unicode strings in the Latin-1 range are being
   shared as well. */
static PyObject *unicode_latin1[256] = {NULL};

unicode_decode_utf8(){
    /*省略*/
    /* ASCII is equivalent to the first 128 ordinals in Unicode. */
    if (size == 1 && (unsigned char)s[0] < 128) {
        if (consumed)
            *consumed = 1;
        return get_latin1_char((unsigned char)s[0]);
    }
    /*省略*/
}


static PyObject*
get_latin1_char(unsigned char ch)
{
    PyObject *unicode = unicode_latin1[ch];
    if (!unicode) {
        unicode = PyUnicode_New(1, ch);
        if (!unicode)
            return NULL;
        PyUnicode_1BYTE_DATA(unicode)[0] = ch;
        assert(_PyUnicode_CheckConsistency(unicode, 1));
        unicode_latin1[ch] = unicode;
    }
    Py_INCREF(unicode);
    return unicode;
}
```

```powershell
In [46]: a = 'p'

In [47]: b = 'p'

In [48]: id(a)
Out[48]: 442757120384

In [49]: id(b)
Out[49]: 442757120384
```

**当然单字符也包括空字符。**

```c++
/* The empty Unicode object is shared to improve performance. */
static PyObject *unicode_empty = NULL;
```

```shell
In [8]: a = 'hello' + 'python'

In [9]: b = 'hellopython'

In [10]: a is b
Out[10]: True

In [11]: a = 'hello ' + 'python'

In [12]: b = 'hello python'

In [13]: id(a)
Out[13]: 118388503536

In [14]: id(b)
Out[14]: 118387544240

In [15]: 'hello ' + 'python' is 'hello python'
Out[15]: False

In [16]: 'hello_' + 'python' is 'hello_python'
Out[16]: True
```



### 2.6 小结：

- **小整数[-5， 257)共用对象，常驻内存**

- **单个字母，长度为 1 的 ascii 的字符[latin1](https://en.wikipedia.org/wiki/ISO/IEC_8859-1)会被interned， 包括空字符，共用对象，常驻内存**

- **由字母、数字、下划线([a-zA-Z0-9_])组成的字符串，不可修改，默认开启intern机制，共用对象，引用计数为0时，销毁**
- 字符串（含有空格），不可修改，没开启intern机制，不共用对象，引用计数为0，销毁

## 3. 标记清除+分代回收

为了防止出现**循环引用**的致命性问题，**python采用的是引用计数机制为主，标记-清除和分代收集两种机制为辅的策略**。

![image.png](https://i.loli.net/2020/06/11/2GI7nmWSPvNjpOR.png)

![image.png](https://i.loli.net/2020/06/11/iLS5ATeBo3W1sVr.png)

我们设置 n1.next 指向 n2，同时设置 n2.prev 指回 n1，现在，我们的两个节点使用循环引用的方式构成了一个`双向链表`，同时请注意到 ABC 以及 DEF 的引用计数值已经增加到了2，现在，假定我们的程序不再使用这两个节点了，我们将 n1 和 n2 都设置为None，Python会像往常一样将每个节点的引用计数减少到1。



![image.png](https://i.loli.net/2020/06/11/q6IpCneRGwt2iM3.png)

### 3.1 在python中的零代(Generation Zero)

Ruby使用一个链表(free_list)来持续追踪未使用的、自由的对象，Python使用一种不同的链表来持续追踪活跃的对象。而不将其称之为“活跃列表”，Python的内部C代码将其称为零代(Generation Zero)。每次当你创建一个对象或其他什么值的时候，Python会将其加入零代链表：

![image.png](https://i.loli.net/2020/06/11/Yp8UMNXmP4ORFDG.png)

从上边可以看到当我们创建ABC节点的时候，Python将其加入零代链表。请注意到这并不是一个真正的列表，并不能直接在你的代码中访问，事实上这个链表是一个完全内部的Python运行时。

***疑惑1：*****对于容器对象(比如list、dict、class、instance等等)，是在什么时候绑定GC，放入第0链表呢？**

相似的，当我们创建DEF节点的时候，Python将其加入同样的链表：

![image.png](https://i.loli.net/2020/06/11/giHxS7pYNKwT8kh.png)

现在零代包含了两个节点对象。(他还将包含Python创建的每个其他值，与一些Python自己使用的内部值。)

### 3.2 标记循环引用

当达到某个 阈值之后 解释器会循环遍历，循环遍历零代列表上的每个对象，检查列表中每个互相引用的对象，根据规则减掉其引用计数。在这个过程中，Python会一个接一个的统计内部引用的数量以防过早地释放对象。以下例子便于理解：

![image.png](https://i.loli.net/2020/06/11/Y1ORJmN2UxPnFg7.png)

从上面可以看到 ABC 和 DEF 节点包含的引用数为1.有三个其他的对象同时存在于零代链表中，蓝色的箭头指示了有一些对象正在被零代链表之外的其他对象所引用。

![image.png](https://i.loli.net/2020/06/11/g1fsLIiYMZupBRo.png)

通过识别内部引用，Python能够减少许多零代链表对象的引用计数。在上图的第一行中你能够看见ABC和DEF的引用计数已经变为零了，这意味着收集器可以释放它们并回收内存空间了。剩下的活跃的对象则被移动到一个新的链表：一代链表。

**疑惑2： 内部如何识别零代的循环引用计数，在什么阈值下会触发GC执行？**



### 3.3 在源码中摸索答案

Python通过`PyGC_Head`来跟踪container对象，`PyGC_Head`信息位于`PyObject_HEAD`之前，定义在`Include/objimpl.h`中

```c++
typedef union _gc_head {
    struct {
        union _gc_head *gc_next;
        union _gc_head *gc_prev;
        Py_ssize_t gc_refs;
    } gc;
    double dummy;  /* force worst-case alignment */
} PyGC_Head;
```

**表头数据结构**

```c++
//Include/internal/mem.h
struct gc_generation {
      PyGC_Head head;
      int threshold; /* collection threshold */  // 阈值
      int count; /* count of allocations or collections of younger
                    generations */    // 实时个数
  };
```

Python中用于分代垃圾收集的三个“代”由`_gc_runtime_state.generations`数组所表示着：

**解答疑惑2，三个代的阈值如下数组**

```c++
/* If we change this, we need to cbhange the default value in the
   signature of gc.collect. */
#define NUM_GENERATIONS 3

_PyGC_Initialize(struct _gc_runtime_state *state)
{
    state->enabled = 1; /* automatic collection enabled? */

#define _GEN_HEAD(n) (&state->generations[n].head)
    struct gc_generation generations[NUM_GENERATIONS] = {
        /* PyGC_Head,                                 threshold,      count */
        {{{_GEN_HEAD(0), _GEN_HEAD(0), 0}},           700,            0},
        {{{_GEN_HEAD(1), _GEN_HEAD(1), 0}},           10,             0},
        {{{_GEN_HEAD(2), _GEN_HEAD(2), 0}},           10,             0},
    };
    for (int i = 0; i < NUM_GENERATIONS; i++) {
        state->generations[i] = generations[i];
    };
    state->generation0 = GEN_HEAD(0);
    struct gc_generation permanent_generation = {
          {{&state->permanent_generation.head, &state->permanent_generation.head, 0}}, 0, 0
    };
    state->permanent_generation = permanent_generation;
}
```

![image.png](https://i.loli.net/2020/06/11/bkKPog8n3Cy1TOx.png)

**解答疑惑1：那container对象是什么时候加入第0“代”的container对象链表呢？**

对于python内置对象的创建，container对象是通过`PyObject_GC_New`函数来创建的，而非container对象是通过`PyObject_Malloc`函数来创建的。

```c++
// Include/objimpl.h
#define PyObject_GC_New(type, typeobj) \
                ( (type *) _PyObject_GC_New(typeobj) )


// 调用了Modules/gcmodule.c中的_PyObject_GC_New函数：
PyObject *
_PyObject_GC_New(PyTypeObject *tp)
{
    PyObject *op = _PyObject_GC_Malloc(_PyObject_SIZE(tp));
    if (op != NULL)
        op = PyObject_INIT(op, tp);
    return op;
}

static PyObject *
_PyObject_GC_Alloc(int use_calloc, size_t basicsize)
{
    PyObject *op;
    PyGC_Head *g;
    size_t size;
    if (basicsize > PY_SSIZE_T_MAX - sizeof(PyGC_Head))
        return PyErr_NoMemory();
    size = sizeof(PyGC_Head) + basicsize;
    // [1]  申请PyGC_Head和对象本身的内存
    if (use_calloc)
        g = (PyGC_Head *)PyObject_Calloc(1, size);
    else
        g = (PyGC_Head *)PyObject_Malloc(size);
    if (g == NULL)
        return PyErr_NoMemory();
    // [2] 设置gc_refs的值
    g->gc.gc_refs = 0;
    _PyGCHead_SET_REFS(g, GC_UNTRACKED);
    // [3]
    generations[0].count++; /* number of allocated GC objects */
    if (generations[0].count > generations[0].threshold &&
        enabled &&
        generations[0].threshold &&
        !collecting &&
        !PyErr_Occurred()) {
        collecting = 1;
        collect_generations();
        collecting = 0;
    }
    // [4]  FROM_GC宏定义可以通过PyGC_Head地址转换PyObject_HEAD地址，逆运算是AS_GC宏定义。
    op = FROM_GC(g);
    return op;
}

PyObject *
_PyObject_GC_Malloc(size_t basicsize)
{
    return _PyObject_GC_Alloc(0, basicsize);
}
```

[4] `FROM_GC`宏定义可以通过`PyGC_Head`地址转换`PyObject_HEAD`地址，逆运算是`AS_GC`宏定义。

```c++
/* Get an object's GC head */
#define AS_GC(o) ((PyGC_Head *)(o)-1)

/* Get the object given the GC head */
#define FROM_GC(g) ((PyObject *)(((PyGC_Head *)g)+1))
```

**当触发阈值后，是如何进行GC回收的？**

`collect`是垃圾回收的主入口函数。**特别注意 finalizers 与 python 的`__del__`绑定了**。

```c
/* This is the main function.  Read this to understand how the
 * collection process works. */
static Py_ssize_t
collect(int generation, Py_ssize_t *n_collected, Py_ssize_t *n_uncollectable,
        int nofail)
{
    int i;
    Py_ssize_t m = 0; /* # objects collected */
    Py_ssize_t n = 0; /* # unreachable objects that couldn't be collected */
    PyGC_Head *young; /* the generation we are examining */
    PyGC_Head *old; /* next older generation */
    PyGC_Head unreachable; /* non-problematic unreachable trash */
    PyGC_Head finalizers;  /* objects with, & reachable from, __del__ */
    PyGC_Head *gc;
    _PyTime_t t1 = 0;   /* initialize to prevent a compiler warning */

    struct gc_generation_stats *stats = &_PyRuntime.gc.generation_stats[generation];
    
    ...

    // “标记-清除”前的准备
    
    // 垃圾标记

    // 垃圾清除
  
    ...

    /* Update stats */
    if (n_collected)
        *n_collected = m;
    if (n_uncollectable)
        *n_uncollectable = n;
    stats->collections++;
    stats->collected += m;
    stats->uncollectable += n;

    if (PyDTrace_GC_DONE_ENABLED())
        PyDTrace_GC_DONE(n+m);

    return n+m;
}
```

### 3.3.1 标记-清除前的准备

```c
    // [1]
    /* update collection and allocation counters */
    if (generation+1 < NUM_GENERATIONS)
        _PyRuntime.gc.generations[generation+1].count += 1;
    for (i = 0; i <= generation; i++)
        _PyRuntime.gc.generations[i].count = 0;

    // [2]
    /* merge younger generations with one we are currently collecting */
    for (i = 0; i < generation; i++) {
        gc_list_merge(GEN_HEAD(i), GEN_HEAD(generation));
    }

    // [3]
    /* handy references */
    young = GEN_HEAD(generation);
    if (generation < NUM_GENERATIONS-1)
        old = GEN_HEAD(generation+1);
    else
        old = young;

    // [4]
    /* Using ob_refcnt and gc_refs, calculate which objects in the
     * container set are reachable from outside the set (i.e., have a
     * refcount greater than 0 when all the references within the
     * set are taken into account).
     */
    update_refs(young);
    subtract_refs(young);
```

[1] 先更新了将被回收的“代”以及老一“代”的count计数器。
这边对老一“代”的count计数器增量1就可以看出来在第1“代”和第2“代”的count值其实表示的是该代垃圾回收的次数。
[2] 通过`gc_list_merge`函数将这些“代”合并成一个链表。

```
/* append list `from` onto list `to`; `from` becomes an empty list */
static void
gc_list_merge(PyGC_Head *from, PyGC_Head *to)
{
    PyGC_Head *tail;
    assert(from != to);
    if (!gc_list_is_empty(from)) {
        tail = to->gc.gc_prev;
        tail->gc.gc_next = from->gc.gc_next;
        tail->gc.gc_next->gc.gc_prev = tail;
        to->gc.gc_prev = from->gc.gc_prev;
        to->gc.gc_prev->gc.gc_next = to;
    }
    gc_list_init(from);
}

static void
gc_list_init(PyGC_Head *list)
{
    list->gc.gc_prev = list;
    list->gc.gc_next = list;
}
```

`gc_list_merge`函数将from链表链接到to链表末尾并把from链表置为空链表。

[3] 经过合并操作之后，所有需要被进行垃圾回收的对象都链接到young“代”（满足超过阈值的最老“代”），并记录old“代”，后面需要将不可回收的对象移到old“代”。

链表的合并操作：

![image.png](https://i.loli.net/2020/06/11/g4QiLXuzaD2eKEo.png)

[4] 寻找root object集合

要对合并的链表进行垃圾标记，首先需要寻找root object集合。
所谓的root object即是一些全局引用和函数栈中的引用。这些引用所用的对象是不可被删除的。

```python
list1 = []
list2 = []
list1.append(list2)
list2.append(list1)
a = list1
del list1
del list2
```

上面的Python中循环引用的代码，变量a所指向的对象就是root object。

三色标记模型

### 3.3.2 垃圾标记

```c
// [1]
/* Leave everything reachable from outside young in young, and move
     * everything else (in young) to unreachable.
     * NOTE:  This used to move the reachable objects into a reachable
     * set instead.  But most things usually turn out to be reachable,
     * so it's more efficient to move the unreachable things.
     */
gc_list_init(&unreachable);
move_unreachable(young, &unreachable);

// [2]
/* Move reachable objects to next generation. */
if (young != old) {
    if (generation == NUM_GENERATIONS - 2) {
        _PyRuntime.gc.long_lived_pending += gc_list_size(young);
    }
    gc_list_merge(young, old);
}
else {
    /* We only untrack dicts in full collections, to avoid quadratic
           dict build-up. See issue #14775. */
    untrack_dicts(young);
    _PyRuntime.gc.long_lived_pending = 0;
    _PyRuntime.gc.long_lived_total = gc_list_size(young);
}
```

[1] 初始化不可达链表，调用`move_unreachable`函数将循环引用的对象移动到不可达链表中：

```c
/* Move the unreachable objects from young to unreachable.  After this,
 * all objects in young have gc_refs = GC_REACHABLE, and all objects in
 * unreachable have gc_refs = GC_TENTATIVELY_UNREACHABLE.  All tracked
 * gc objects not in young or unreachable still have gc_refs = GC_REACHABLE.
 * All objects in young after this are directly or indirectly reachable
 * from outside the original young; and all objects in unreachable are
 * not.
 */
static void
move_unreachable(PyGC_Head *young, PyGC_Head *unreachable)
{
    PyGC_Head *gc = young->gc.gc_next;

    /* Invariants:  all objects "to the left" of us in young have gc_refs
     * = GC_REACHABLE, and are indeed reachable (directly or indirectly)
     * from outside the young list as it was at entry.  All other objects
     * from the original young "to the left" of us are in unreachable now,
     * and have gc_refs = GC_TENTATIVELY_UNREACHABLE.  All objects to the
     * left of us in 'young' now have been scanned, and no objects here
     * or to the right have been scanned yet.
     */

    while (gc != young) {
        PyGC_Head *next;

        if (_PyGCHead_REFS(gc)) {
            /* gc is definitely reachable from outside the
             * original 'young'.  Mark it as such, and traverse
             * its pointers to find any other objects that may
             * be directly reachable from it.  Note that the
             * call to tp_traverse may append objects to young,
             * so we have to wait until it returns to determine
             * the next object to visit.
             */
            PyObject *op = FROM_GC(gc);
            traverseproc traverse = Py_TYPE(op)->tp_traverse;
            assert(_PyGCHead_REFS(gc) > 0);
            _PyGCHead_SET_REFS(gc, GC_REACHABLE);
            (void) traverse(op,
                            (visitproc)visit_reachable,
                            (void *)young);
            next = gc->gc.gc_next;
            if (PyTuple_CheckExact(op)) {
                _PyTuple_MaybeUntrack(op);
            }
        }
        else {
            /* This *may* be unreachable.  To make progress,
             * assume it is.  gc isn't directly reachable from
             * any object we've already traversed, but may be
             * reachable from an object we haven't gotten to yet.
             * visit_reachable will eventually move gc back into
             * young if that's so, and we'll see it again.
             */
            next = gc->gc.gc_next;
            gc_list_move(gc, unreachable);
            _PyGCHead_SET_REFS(gc, GC_TENTATIVELY_UNREACHABLE);
        }
        gc = next;
    }
}
```

这边遍历young“代”的container对象链表，`_PyGCHead_REFS(gc)`判断是不是root object或从某个root object能直接/间接引用的对象，由于root object集合中的对象是不能回收的，因此，被这些对象直接或间接引用的对象也是不能回收的。

`_PyGCHead_REFS(gc)`为0并不能断定这个对象是可回收的，但是还是先移动到`unreachable`链表中，设置了`GC_TENTATIVELY_UNREACHABLE`标志表示暂且认为是不可达的，如果是存在被root object直接或间接引用的对象，这样的对象还会被移出`unreachable`链表中。

[2] 将可达的对象移到下一“代”。

### 3.3.3 垃圾清除

```c
// [1]
    /* All objects in unreachable are trash, but objects reachable from
     * legacy finalizers (e.g. tp_del) can't safely be deleted.
     */
    gc_list_init(&finalizers);
    move_legacy_finalizers(&unreachable, &finalizers);
    /* finalizers contains the unreachable objects with a legacy finalizer;
     * unreachable objects reachable *from* those are also uncollectable,
     * and we move those into the finalizers list too.
     */
    move_legacy_finalizer_reachable(&finalizers);

    // [2]
    /* Collect statistics on collectable objects found and print
     * debugging information.
     */
    for (gc = unreachable.gc.gc_next; gc != &unreachable;
                    gc = gc->gc.gc_next) {
        m++;
    }

    // [3]
    /* Clear weakrefs and invoke callbacks as necessary. */
    m += handle_weakrefs(&unreachable, old);

    // [4]
    /* Call tp_finalize on objects which have one. */
    finalize_garbage(&unreachable);

    // [5]
    if (check_garbage(&unreachable)) {
        revive_garbage(&unreachable);
        gc_list_merge(&unreachable, old);
    }
    else {
        /* Call tp_clear on objects in the unreachable set.  This will cause
         * the reference cycles to be broken.  It may also cause some objects
         * in finalizers to be freed.
         */
        delete_garbage(&unreachable, old);
    }
    
    // [6]
    /* Collect statistics on uncollectable objects found and print
     * debugging information. */
    for (gc = finalizers.gc.gc_next;
         gc != &finalizers;
         gc = gc->gc.gc_next) {
        n++;
    }
    
    ...

    // [7]
    /* Append instances in the uncollectable set to a Python
     * reachable list of garbage.  The programmer has to deal with
     * this if they insist on creating this type of structure.
     */
    (void)handle_legacy_finalizers(&finalizers, old);
    
    /* Clear free list only during the collection of the highest
     * generation */
    if (generation == NUM_GENERATIONS-1) {
        clear_freelists();
    }
```

[1] 处理`unreachable`链表中有finalizer的对象。即python中 实现了`__del__`魔法方法的对象

```c
/* Move the objects in unreachable with tp_del slots into `finalizers`.
 * Objects moved into `finalizers` have gc_refs set to GC_REACHABLE; the
 * objects remaining in unreachable are left at GC_TENTATIVELY_UNREACHABLE.
 */
static void
move_legacy_finalizers(PyGC_Head *unreachable, PyGC_Head *finalizers)
{
    PyGC_Head *gc;
    PyGC_Head *next;

    /* March over unreachable.  Move objects with finalizers into
     * `finalizers`.
     */
    for (gc = unreachable->gc.gc_next; gc != unreachable; gc = next) {
        PyObject *op = FROM_GC(gc);

        assert(IS_TENTATIVELY_UNREACHABLE(op));
        next = gc->gc.gc_next;

        if (has_legacy_finalizer(op)) {
            gc_list_move(gc, finalizers);
            _PyGCHead_SET_REFS(gc, GC_REACHABLE);
        }
    }
}
```

遍历`unreachable`链表，将拥有finalizer的实例对象移到`finalizers`链表中，并标示为`GC_REACHABLE`。

```c
/* Return true if object has a pre-PEP 442 finalization method. */
static int
has_legacy_finalizer(PyObject *op)
{
    return op->ob_type->tp_del != NULL;
}
```

**拥有finalizer的实例对象指的就是实现了`tp_del`函数的对象。**

```c
/* Move objects that are reachable from finalizers, from the unreachable set
 * into finalizers set.
 */
static void
move_legacy_finalizer_reachable(PyGC_Head *finalizers)
{
    traverseproc traverse;
    PyGC_Head *gc = finalizers->gc.gc_next;
    for (; gc != finalizers; gc = gc->gc.gc_next) {
        /* Note that the finalizers list may grow during this. */
        traverse = Py_TYPE(FROM_GC(gc))->tp_traverse;
        (void) traverse(FROM_GC(gc),
                        (visitproc)visit_move,
                        (void *)finalizers);
    }
}
```

对`finalizers`链表中拥有finalizer的实例对象遍历其引用对象，调用`visit_move`访问者，这些被引用的对象也不应该被释放。

```c
/* A traversal callback for move_legacy_finalizer_reachable. */
static int
visit_move(PyObject *op, PyGC_Head *tolist)
{
    if (PyObject_IS_GC(op)) {
        if (IS_TENTATIVELY_UNREACHABLE(op)) {
            PyGC_Head *gc = AS_GC(op);
            gc_list_move(gc, tolist);
            _PyGCHead_SET_REFS(gc, GC_REACHABLE);
        }
    }
    return 0;
}

#define IS_TENTATIVELY_UNREACHABLE(o) ( \
    _PyGC_REFS(o) == GC_TENTATIVELY_UNREACHABLE)
```

`visit_move`函数将引用对象还在`unreachable`链表的对象移到`finalizers`链表中。

[2] 统计`unreachable`链表数量。
[3] 处理弱引用。
[4] [5] 开始清除垃圾对象，我们先只看`delete_garbage`函数：

```c
/* Break reference cycles by clearing the containers involved.  This is
 * tricky business as the lists can be changing and we don't know which
 * objects may be freed.  It is possible I screwed something up here.
 */
static void
delete_garbage(PyGC_Head *collectable, PyGC_Head *old)
{
    inquiry clear;

    while (!gc_list_is_empty(collectable)) {
        PyGC_Head *gc = collectable->gc.gc_next;
        PyObject *op = FROM_GC(gc);

        if (_PyRuntime.gc.debug & DEBUG_SAVEALL) {
            PyList_Append(_PyRuntime.gc.garbage, op);
        }
        else {
            if ((clear = Py_TYPE(op)->tp_clear) != NULL) {
                Py_INCREF(op);
                clear(op);
                Py_DECREF(op);
            }
        }
        if (collectable->gc.gc_next == gc) {
            /* object is still alive, move it, it may die later */
            gc_list_move(gc, old);
            _PyGCHead_SET_REFS(gc, GC_REACHABLE);
        }
    }
}
```

遍历`unreachable`链表中的container对象，调用其类型对象的`tp_clear`指针指向的函数，我们以list对象为例：

```c
static int
_list_clear(PyListObject *a)
{
    Py_ssize_t i;
    PyObject **item = a->ob_item;
    if (item != NULL) {
        /* Because XDECREF can recursively invoke operations on
           this list, we make it empty first. */
        i = Py_SIZE(a);
        Py_SIZE(a) = 0;
        a->ob_item = NULL;
        a->allocated = 0;
        while (--i >= 0) {
            Py_XDECREF(item[i]);
        }
        PyMem_FREE(item);
    }
    /* Never fails; the return value can be ignored.
       Note that there is no guarantee that the list is actually empty
       at this point, because XDECREF may have populated it again! */
    return 0;
}
```

`_list_clear`函数对container对象的每个元素进行引用数减量操作并释放container对象内存。

`delete_garbage`在对container对象进行`clear`操作之后，还会检查是否成功，如果该container对象没有从`unreachable`链表上摘除，表示container对象还不能销毁，需要放回到老一“代”中，并标记`GC_REACHABLE`。

[6] 统计`finalizers`链表数量。
[7] 处理`finalizers`链表的对象。

```c
/* Handle uncollectable garbage (cycles with tp_del slots, and stuff reachable
 * only from such cycles).
 * If DEBUG_SAVEALL, all objects in finalizers are appended to the module
 * garbage list (a Python list), else only the objects in finalizers with
 * __del__ methods are appended to garbage.  All objects in finalizers are
 * merged into the old list regardless.
 * Returns 0 if all OK, <0 on error (out of memory to grow the garbage list).
 * The finalizers list is made empty on a successful return.
 */
static int
handle_legacy_finalizers(PyGC_Head *finalizers, PyGC_Head *old)
{
    PyGC_Head *gc = finalizers->gc.gc_next;

    if (_PyRuntime.gc.garbage == NULL) {
        _PyRuntime.gc.garbage = PyList_New(0);
        if (_PyRuntime.gc.garbage == NULL)
            Py_FatalError("gc couldn't create gc.garbage list");
    }
    for (; gc != finalizers; gc = gc->gc.gc_next) {
        PyObject *op = FROM_GC(gc);

        if ((_PyRuntime.gc.debug & DEBUG_SAVEALL) || has_legacy_finalizer(op)) {
            if (PyList_Append(_PyRuntime.gc.garbage, op) < 0)
                return -1;
        }
    }

    gc_list_merge(finalizers, old);
    return 0;
}
```

遍历`finalizers`链表，将拥有finalizer的实例对象放到一个名为garbage的PyListObject对象中，可以通过gc模块查看。

```powershell
>>> import gc
>>> gc.garbage
```

并把`finalizers`链表晋升到老一“代”。

> **注意：`__del__`给gc带来的影响, gc模块唯一处理不了的是循环引用的类都有`__del__`方法，所以项目中要避免定义[`__del__`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__del__)方法 ** [官方警告](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__del__)

### 3.4 小结

1. GC的流程:

   ```
   -> 发现超过阈值了
   -> 触发垃圾回收
   -> 将所有可达对象链表放到一起
   -> 遍历, 计算有效引用计数
   -> 分成 有效引用计数=0 和 有效引用计数 > 0 两个集合
   -> 大于0的, 放入到更老一代
   -> =0的, 执行回收
   -> 回收遍历容器内的各个元素, 减掉对应元素引用计数(破掉循环引用)
   -> 执行-1的逻辑, 若发现对象引用计数=0, 触发内存回收
   -> 由python底层内存管理机制回收内存
   ```

2. 触发GC的条件

   - 主动调用`gc.collect(),`

   - 当gc模块的计数器达到阀值的时候

   - 程序退出的时候



## 4. GC阈值

**分代回收   以空间换时间**

> **重要思想**：将系统中的所有内存块根据其存活的时间划分为不同的集合, 每个集合就成为一个”代”, 垃圾收集的频率随着”代”的存活时间的增大而减小(活得越长的对象, 就越不可能是垃圾, 就应该减少去收集的频率)

**弱代假说**

分代垃圾回收算法的核心行为：垃圾回收器会更频繁的处理新对象。一个新的对象即是你的程序刚刚创建的，而一个来的对象则是经过了几个时间周期之后仍然存在的对象。Python会在当一个对象从零代移动到一代，或是从一代移动到二代的过程中提升`(promote)`这个对象。

**为什么要这么做？**这种算法的根源来自于弱代假说(**weak generational hypothesis**)。这个假说由两个观点构成：

> 首先是年亲的对象通常死得也快，而老对象则很有可能存活更长的时间。

假定我们创建了一个Python创建：

```python
n1 = Node("ABC")
```

根据假说，我的代码很可能仅仅会使用ABC很短的时间。这个对象也许仅仅只是一个方法中的中间结果，并且随着方法的返回这个对象就将变成垃圾了。大部分的新对象都是如此般地很快变成垃圾。然而，偶尔程序会创建一些很重要的，存活时间比较长的对象-例如web应用中的session变量或是配置项。

> 通过频繁的处理零代链表中的新对象，Python的垃圾收集器将把时间花在更有意义的地方：它处理那些很快就可能变成垃圾的新对象。同时只在很少的时候，当满足阈值的条件，收集器才回去处理那些老变量。



## 5. Python中的gc模块使用

> gc模块默认是开启自动回收垃圾的，`gc.isenabled()=True`

**常用函数:** 

- `gc.set_debug(flags)` 设置gc的debug日志，一般设置为`gc.DEBUG_LEAK`

```python

"""
DEBUG_STATS - 在垃圾收集过程中打印所有统计信息
DEBUG_COLLECTABLE - 打印发现的可收集对象
DEBUG_UNCOLLECTABLE - 打印unreachable对象(除了uncollectable对象)
DEBUG_SAVEALL - 将对象保存到gc.garbage(一个列表)里面，而不是释放它
DEBUG_LEAK - 对内存泄漏的程序进行debug (everything but STATS).
    
"""
```

- `gc.collect([generation])` 显式进行垃圾回收，可以输入参数，0代表只检查第一代的对象，1代表检查一，二代的对象，2代表检查一，二，三代的对象，如果不传参数，执行一个full collection，也就是等于传2。 返回不可达（unreachable objects）对象的数目

- `gc.get_threshold() `获取的gc模块中自动执行垃圾回收的频率

- `gc.get_stats()`查看每一代的具体信息

- `gc.set_threshold(threshold0[, threshold1[, threshold2])` 设置自动执行垃圾回收的频率

- `gc.get_count() `获取当前自动执行垃圾回收的计数器，返回一个长度为3的列表

  例如**(488,3,0)**，其中488是指距离上一次一代垃圾检查，Python分配内存的数目减去释放内存的数目，注意是内存分配，而不是引用计数的增加。

  3是指距离上一次二代垃圾检查，一代垃圾检查的次数，同理，0是指距离上一次三代垃圾检查，二代垃圾检查的次数。

**计数器和阈值关系解释：**

```python
当计数器从(699,3,0)增加到(700,3,0)，gc模块就会执行gc.collect(0),即检查一代对象的垃圾，并重置计数器为(0,4,0)
当计数器从(699,9,0)增加到(700,9,0)，gc模块就会执行gc.collect(1),即检查一、二代对象的垃圾，并重置计数器为(0,0,1)
当计数器从(699,9,9)增加到(700,9,9)，gc模块就会执行gc.collect(2),即检查一、二、三代对象的垃圾，并重置计数器为(0,0,0)
```

## 6. 工作中如何避免循环引用？

> To avoid circular references in your code, you can use weak references, that are implemented in the `weakref` module. Unlike the usual references, the `weakref.ref` doesn't increase the reference count and returns `None` if an object was destroyed. [rushter](https://rushter.com/blog/python-garbage-collector/)

```python
import weakref


class Node():
    def __init__(self, value):
        self.value = value
        self._parent = None
        self.children = []

    def __repr__(self):
        return 'Node({!r:})'.format(self.value)

    @property
    def parent(self):
        return None if self._parent is None else self._parent()

    @parent.setter
    def parent(self, node):
        self._parent = weakref.ref(node)

    def add_child(self, child):
        self.children.append(child)
        child.parent = self


if __name__ == '__main__':

    a = Data()
    del a

    a = Node()
    del a

    a = Node()
    a.add_child(Node())
    del a
```

> 弱引用消除了引用循环的这个问题，本质来讲，**弱引用就是一个对象指针，它不会增加它的引用计数**

> 弱引用的主要用途是实现保存大对象的高速缓存或映射，但又并希望大对象仅仅因为它出现在高速缓存或映射中而保持存活

为了访问弱引用所引用的对象，你可以像函数一样去调用它即可。如果那个对象还存在就会返回它，否则就返回一个None。 由于原始对象的引用计数没有增加，那么就可以去删除它了

并非所有对象都可以被弱引用；可以被弱引用的对象包括类实例，用 Python（而不是用 C）编写的函数，实例方法、集合、冻结集合，某些 [文件对象](https://docs.python.org/zh-cn/3/glossary.html#term-file-object)，[生成器](https://docs.python.org/zh-cn/3/glossary.html#term-generator)，类型对象，套接字，数组，双端队列，正则表达式模式对象以及代码对象等。

几个内建类型如 [`list`](https://docs.python.org/zh-cn/3/library/stdtypes.html#list) 和 [`dict`](https://docs.python.org/zh-cn/3/library/stdtypes.html#dict) 不直接支持弱引用，但可以通过子类化添加支持:

```
class Dict(dict):
    pass

obj = Dict(red=1, green=2, blue=3)   # this object is weak referenceable
```

其他内置类型例如 [`tuple`](https://docs.python.org/zh-cn/3/library/stdtypes.html#tuple) 和 [`int`](https://docs.python.org/zh-cn/3/library/functions.html#int) 不支持弱引用，即使通过子类化也不支持



**python官方推荐弱引用代替[`__del__`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__del__)方法**

假设我们想创建一个类，用它的实例来代表临时目录。 当以下事件中的某一个发生时，这个目录应当与其内容一起被删除：

- 对象被作为垃圾回收，
- 对象的 `remove()` 方法被调用，或
- 程序退出。

原本用`__del__()`方法

```python
class TempDir:
    def __init__(self):
        self.name = tempfile.mkdtemp()
       
   	def __remove(self):
        if self.name is not None:
            shutil.rmtree(self.name)
            self.name = None
    
    @property
    def removed(self):
        return self.name is None
   
	def __del__(self):
        self.__remove()
```

更健壮的替代方式可以是定义一个终结器，只引用它所需要的特定函数和对象，而不是获取对整个对象状态的访问权:

```python
class TempDir:
    def __init__(self):
        self.name = tempfile.mkdtemp()
        self._finalizer = weakref.finalize(self, shutil.rmtree, self.name)
       
   	def remove(self):
        self._finalizer()
    
    @property
    def removed(self):
        return not self._finalizer.alive
```

像这样定义后，我们的终结器将只接受一个对其完成正确清理目录任务所需细节的引用。 如果对象一直未被作为垃圾回收，终结器仍会在退出时被调用.[weakref](https://docs.python.org/zh-cn/3/library/weakref.html#module-weakref)



**参考文章和书籍:**

1. [visualizing garbage collection in ruby and python](http://patshaughnessy.net/2013/10/24/visualizing-garbage-collection-in-ruby-and-python)
2. [膜拜的大佬-Junnplus'blog](https://github.com/Junnplus/blog/issues/19)
3. [wklken前辈](http://wklken.me/posts/2015/09/29/python-source-gc.html)
4. [The Garbage Collector](https://pythoninternal.wordpress.com/2014/08/04/the-garbage-collector/)
5. [Garbage collection in Python: things you need to know](https://rushter.com/blog/python-garbage-collector/)
6. [Python-CookBook-循环引用数据结构的内存管理](https://python3-cookbook.readthedocs.io/zh_CN/latest/c08/p23_managing_memory_in_cyclic_data_structures.html)
7. 《python源码剖析》
8. Python-3.8.3/Modules/gcmodule.c

