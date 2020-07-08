## Python3 源码阅读 数据类型-Int

Python3支持Int, float,  complex三种Number数据类型，其中bool（Booleans）为int型的子类

```powershell
>>> True == 1 == 1.0
True
>>> (hash(True), hash(1), hash(1.0))
(1, 1, 1)
```

> “The Boolean type is a subtype of the integer type, and Boolean values behave like the values 0 and 1, respectively, in almost all contexts, the exception being that when converted to a string, the strings ‘False’ or ‘True’ are returned, respectively.”
>
> “布尔类型是整数类型的一个子类型，在几乎所有的上下文环境中布尔值的行为类似于值0和1，例外的是当转换为字符串时，会分别将字符串”False“或”True“返回。“（[原文](https://docs.python.org/3/reference/datamodel.html#the-standard-type-hierarchy)）
>
> **就python而言，`True`，`1`和`1.0`都表示相同的字典键**

以上描述来自 [一个Python字典表达式谜题](https://vimiix.com/post/2017/12/28/python-mystery-dict-expression/#5ab0ed06ee920a00454446ee)



在Python 2中，分别使用`intobject`和`longobject`去存储整型，而在Python 3中，则使用`longobject`统一的表示整型，并且将type也设为“int”，在[PEP 237 – Unifying Long Integers and Integers](https://www.python.org/dev/peps/pep-0237/)中，详细的阐述了这个改变

```c++
typedef struct _longobject PyLongObject; /* Revealed in longintrepr.h */
```

```c++
/* Long integer representation.
   The absolute value of a number is equal to
    SUM(for i=0 through abs(ob_size)-1) ob_digit[i] * 2**(SHIFT*i)
   Negative numbers are represented with ob_size < 0;
   zero is represented by ob_size == 0.
   In a normalized number, ob_digit[abs(ob_size)-1] (the most significant
   digit) is never zero.  Also, in all cases, for all valid i,
    0 <= ob_digit[i] <= MASK.
   The allocation function takes care of allocating extra memory
   so that ob_digit[0] ... ob_digit[abs(ob_size)-1] are actually available.

   CAUTION:  Generic code manipulating subtypes of PyVarObject has to
   aware that ints abuse  ob_size's sign bit.
*/

struct _longobject {
    PyObject_VAR_HEAD
    digit ob_digit[1]; 
};
```

- 整数的绝对值为`SUM(for i=0 through abs(ob_size)-1) ob_digit[i] * 2**(SHIFT*i)`
- **整数0**：当要表示的整数的值为 0 时, **ob_digit** 这个数组为空, 不存储任何东西, **ob_size** 中的 0 就直接表示这个整数的值为 0, 这是一种特殊情况
- 对于正常的数，`ob_digit[abs(ob_size)-1]`, 且`0 <= ob_digit[i] <= MASK`
- 负数的`ob_size` < 0，即正负符号信息由ob_size保存



**疑惑？，其中 `digit ob_digit[1];`是什么东西，有什么作用？**

有待解惑：[junnplus](https://github.com/Junnplus/blog/issues/12#)  [柔性数组](https://github.com/Junnplus/blog/issues/12#issuecomment-431687478)

[Understanding memory allocation for large integers in Python](https://stackoverflow.com/questions/40344159/understanding-memory-allocation-for-large-integers-in-python)

[Why use array size 1 instead of pointer?](https://stackoverflow.com/questions/6390331/why-use-array-size-1-instead-of-pointer/6390357#6390357)



### 小整数对象池- samll-ints

cpython 同时也使用了一个全局变量叫做 small_ints 来单例化一部分常见范围的整数, 这么做可以减少频繁的向操作系统申请和释放的次数, 并提高性能

```c++
#ifndef NSMALLPOSINTS
#define NSMALLPOSINTS           257
#endif
#ifndef NSMALLNEGINTS
#define NSMALLNEGINTS           5
#endif

// ... ...

/* Small integers are preallocated in this array so that they
   can be shared.
   The integers that are preallocated are those in the range
   -NSMALLNEGINTS (inclusive) to NSMALLPOSINTS (not inclusive).
*/
static PyLongObject small_ints[NSMALLNEGINTS + NSMALLPOSINTS];
```

