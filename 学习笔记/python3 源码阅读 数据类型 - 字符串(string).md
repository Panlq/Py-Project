# python3 源码阅读 数据类型 - 字符串(string)

相关文件

> Objects/unicodeobject.c
>
> Objects/codeobject.c



## 字符串连接

Python中的字符串`"+"`操作对应的就是`PyUnicode_Concat`函数

```c++
/* Concat to string or Unicode object giving a new Unicode object. */

PyObject *
PyUnicode_Concat(PyObject *left, PyObject *right)
{
    PyObject *result;
    Py_UCS4 maxchar, maxchar2;
    Py_ssize_t left_len, right_len, new_len;

    if (ensure_unicode(left) < 0)
        return NULL;

    if (!PyUnicode_Check(right)) {
        PyErr_Format(PyExc_TypeError,
                     "can only concatenate str (not \"%.200s\") to str",
                     right->ob_type->tp_name);
        return NULL;
    }
    if (PyUnicode_READY(right) < 0)
        return NULL;

    /* Shortcuts */
    if (left == unicode_empty)
        return PyUnicode_FromObject(right);
    if (right == unicode_empty)
        return PyUnicode_FromObject(left);

    left_len = PyUnicode_GET_LENGTH(left);
    right_len = PyUnicode_GET_LENGTH(right);
    if (left_len > PY_SSIZE_T_MAX - right_len) {
        PyErr_SetString(PyExc_OverflowError,
                        "strings are too large to concat");
        return NULL;
    }
    // [1]
    new_len = left_len + right_len;

    maxchar = PyUnicode_MAX_CHAR_VALUE(left);
    maxchar2 = PyUnicode_MAX_CHAR_VALUE(right);
    maxchar = Py_MAX(maxchar, maxchar2);

    /* Concat the two Unicode strings */
    // [2]
    result = PyUnicode_New(new_len, maxchar);
    if (result == NULL)
        return NULL;
    // [3]
    _PyUnicode_FastCopyCharacters(result, 0, left, 0, left_len);
    _PyUnicode_FastCopyCharacters(result, left_len, right, 0, right_len);
    assert(_PyUnicode_CheckConsistency(result, 1));
    return result;
}
```

因为字符串对象是不可变对象，进行连接操作是会创建一个新的字符串对象。所以两字符串对象连接`[1]`会先计算连接后字符串的长度，`[2]`通过`PyUnicode_New`来申请内存空间，最后`[3]`复制两字符串的内存空间数据。

这种连接操作作用在N个字符串对象上就显得非常低效率，连接N个字符串对象就需要进行`N-1`次的内存申请和`(N-1)*2`次的内存搬运工作，另外还有隐藏的垃圾回收操作。更好的做法是通过`join`操作来连接。

```c++
PyUnicode_Join(PyObject *separator, PyObject *seq)
{
    PyObject *res;
    PyObject *fseq;
    Py_ssize_t seqlen;
    PyObject **items;

    fseq = PySequence_Fast(seq, "can only join an iterable");
    if (fseq == NULL) {
        return NULL;
    }

    /* NOTE: the following code can't call back into Python code,
     * so we are sure that fseq won't be mutated.
     */

    items = PySequence_Fast_ITEMS(fseq);
    seqlen = PySequence_Fast_GET_SIZE(fseq);
    res = _PyUnicode_JoinArray(separator, items, seqlen);
    Py_DECREF(fseq);
    return res;
}
```

`PySequence_Fast_GET_SIZE` 计算序列所有元素字符串总长度，使用`res = PyUnicode_New(sz, maxchar);`分配内存空间, 然后逐一拷贝. 一次内存操作。

## 字符串hash

变量其作用是缓存该对象的 HASH 值,这样可以避免每一次都重新计算该字符串对象的 HASH 值。如果一个 `PyUnicodeObject`对象还没有被计算过 HASH 值,那么 `ob_hash` 的初始值是-1