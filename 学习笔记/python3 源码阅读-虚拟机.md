## python3 源码阅读-python虚拟机

> 阅读源码版本python 3.8.3
>
> 参考书籍<<Python源码剖析>>

[官网文档目录介绍](https://devguide.python.org/setup/)

1. Doc目录主要是官方文档的说明。

2. Include目录主要包括了Python的运行的头文件。

3. Lib目录主要包括了用Python实现的标准库。

4. Objects目录包括了内建对象。

5. Parser目录包括了python编译相关代码，将python文件编译生成语法树等相关工作。

6. Programs目录主要包括了python的入口函数。

7. Python目录主要包括了Python动态运行时执行的代码，里面包括编译、字节码解释器等工作。
   

### Run Python文件的启动流程

Python启动是由Programs下的python.c文件中的main函数开始执行

```c
/* Minimal main program -- everything is loaded from the library */

#include "Python.h"
#include "pycore_pylifecycle.h"

#ifdef MS_WINDOWS
int
wmain(int argc, wchar_t **argv)
{
    return Py_Main(argc, argv);
}
#else
int
main(int argc, char **argv)
{
    return Py_BytesMain(argc, argv);
}
#endif
```

```c++
int
Py_Main(int argc, wchar_t **argv) {
    ...
    return pymian_main(&args);
}

static int
pymain_main(_PyArgv *args)
{
    PyStatus status = pymain_init(args);  // 初始化
    if (_PyStatus_IS_EXIT(status)) {
        pymain_free();
        return status.exitcode;
    }
    if (_PyStatus_EXCEPTION(status)) {
        pymain_exit_error(status);
    }

    return Py_RunMain();
}
```

>  Python3.8 对Python解释器的初始化做了重构[PEP 587-Python初始化配置](https://www.python.org/dev/peps/pep-0587/)

#### 1. 初始化关键流程

- 初始化一些与配置项 如:开启utf-8模式,设置Python内存分配器
- 初始化`pyinit_core`核心部分
  - 创建生命周期 `pycore_init_runtime`,  同时生成HashRandom
  - 初始化线程和解释器并创建GIL锁 `pycore_create_interpreter`
  - 初始化所有基础类型，list, int, tuple等  `pycore_init_types`
  - 初始化sys模块  `_PySys_Create`
  - 初始化内建函数或者对象，如map, None, True等 `pycore_init_builtins`
    - 其中包括内建的错误类型初始化 `_PyBuiltins_AddExceptions`

> 

#### 2. 执行文件

```c
int
Py_RunMain(void)
{
    int exitcode = 0;
	
    pymain_run_python(&exitcode);  //执行python脚本

	if (Py_FinalizeEx() < 0) {  // 释放资源
        /* Value unlikely to be confused with a non-error exit status or
           other special meaning */
        exitcode = 120;
    }

    pymain_free();   // 释放资源

    if (_Py_UnhandledKeyboardInterrupt) {
        exitcode = exit_sigint();
    }

    return exitcode;
}


static void
pymain_run_python(int *exitcode)
{   
    // 获取一个持有GIL锁的解释器
    PyInterpreterState *interp = _PyInterpreterState_GET_UNSAFE();
    /* pymain_run_stdin() modify the config */
    ... // 添加sys_path等操作

    if (config->run_command) {
        // 命令行模式
        *exitcode = pymain_run_command(config->run_command, &cf); 
    }
    else if (config->run_module) {
        // 模块名
        *exitcode = pymain_run_module(config->run_module, 1);
    }
    else if (main_importer_path != NULL) {
        *exitcode = pymain_run_module(L"__main__", 0);
    }
    else if (config->run_filename != NULL) {
        // 文件名
        *exitcode = pymain_run_file(config, &cf);
    }
    else {
        *exitcode = pymain_run_stdin(config, &cf);
    }

	...
}

/* Parse input from a file and execute it */ //Python/pythonrun.c
int
PyRun_AnyFileExFlags(FILE *fp, const char *filename, int closeit,
                     PyCompilerFlags *flags)
{
    if (filename == NULL)
        filename = "???";
    if (Py_FdIsInteractive(fp, filename)) {
        int err = PyRun_InteractiveLoopFlags(fp, filename, flags);  // 是否是交互模式
        if (closeit)
            fclose(fp);
        return err;
    }
    else
        return PyRun_SimpleFileExFlags(fp, filename, closeit, flags);   // 执行脚本
}


int
PyRun_SimpleFileExFlags(FILE *fp, const char *filename, int closeit,
                        PyCompilerFlags *flags)
{
    ...
    if (maybe_pyc_file(fp, filename, ext, closeit)) {
        FILE *pyc_fp;
        /* Try to run a pyc file. First, re-open in binary */
        ...
        v = run_pyc_file(pyc_fp, filename, d, d, flags);
    } else {
        /* When running from stdin, leave __main__.__loader__ alone */
        ...
        v = PyRun_FileExFlags(fp, filename, Py_file_input, d, d,
                              closeit, flags);
    }
    ...
}

PyObject *
PyRun_FileExFlags(FILE *fp, const char *filename_str, int start, PyObject *globals,
                  PyObject *locals, int closeit, PyCompilerFlags *flags)
{
    ...
    // // 解析传入的脚本，解析成AST
    mod = PyParser_ASTFromFileObject(fp, filename, NULL, start, 0, 0,
                                     flags, NULL, arena); 
    ...
    // 将AST编译成字节码然后启动字节码解释器执行编译结果
    ret = run_mod(mod, filename, globals, locals, flags, arena);
    ...
}

// 查看run_mode
static PyObject *
run_mod(mod_ty mod, PyObject *filename, PyObject *globals, PyObject *locals,
            PyCompilerFlags *flags, PyArena *arena)
{
    ...
    // 将AST编译成字节码
    co = PyAST_CompileObject(mod, filename, flags, -1, arena);  
    ...

    // 解释执行编译的字节码
    v = run_eval_code_obj(co, globals, locals);
    Py_DECREF(co);
    return v;
}
```

再将AST转换为字节码后，调用了PyEval_EvalCode来执行字节码，查看位于Python/ceval.c中的该函数，最终调用了PyEval_EvalFrameEx来执行，该函数就是字节码解释器，实现方式就是一个for循序依次执行字节码，然后调用相关函数去执行，解释出来的脚本，然后返回执行结果。

#### 3. 总结流程图

![image-20200608163433117.png](https://i.loli.net/2020/06/08/LMXfyB8ipJbwTuE.png)

#### 4. 案例

新建test.py

```python
a = 10
print(a)
```

执行命令: `python3 -m dis test.py`

```powershell
λ python3 -m dis test.py
  1           0 LOAD_CONST               0 (10)
              2 STORE_NAME               0 (a)

  2           4 LOAD_NAME                1 (print)
              6 LOAD_NAME                0 (a)
              8 CALL_FUNCTION            1
             10 POP_TOP
             12 LOAD_CONST               1 (None)
             14 RETURN_VALUE

```

左边1和2表示 test.py中的第一行和第二行，第二列表示python byte code

 `Include/opcode.h` 发现总共有 163 个 opcode, 所有的 python 源文件都会被编译器翻译成由 opcode 组成的 pyx 文件，并**缓存**在执行目录，下次启动程序**如果源代码没有修改过，则直接加载这个pyx文件，这个文件的存在可以加快 python 的加载速度**

```c++
// Python\ceval.c
main_loop:
    for (;;) {
        ...
            
        switch (opcode) {
 
        /* BEWARE!
           It is essential that any operation that fails must goto error
           and that all operation that succeed call [FAST_]DISPATCH() ! */
 
        case TARGET(NOP): {
            FAST_DISPATCH();
        }
 
        case TARGET(LOAD_FAST): {
            PyObject *value = GETLOCAL(oparg);
            if (value == NULL) {
                format_exc_check_arg(PyExc_UnboundLocalError,
                                     UNBOUNDLOCAL_ERROR_MSG,
                                     PyTuple_GetItem(co->co_varnames, oparg));
                goto error;
            }
            Py_INCREF(value);
            PUSH(value);
            FAST_DISPATCH();
        }
 
        case TARGET(LOAD_CONST): {
            PREDICTED(LOAD_CONST);
            PyObject *value = GETITEM(consts, oparg);
            Py_INCREF(value);
            PUSH(value);
            FAST_DISPATCH();
        }
        ...
    }
}
```

在 python 虚拟机中，解释器主要在一个很大的循环中，不停地读入 opcode, 并根据 opcode 执行对应的指令，当执行完所有指令虚拟机退出，程序也就结束了

##### 4.1 LOAD_CONST

```c
// Python\ceval.c
PREDICTED(LOAD_CONST);     -> line 943: #define PREDICTED(op)           PRED_##op:
FAST_DISPATCH();           -> line 876 #define FAST_DISPATCH() goto fast_next_opcode
```

> 额外收获: c 语言中  ##和# 号 在marco 里的作用可以参考 [这篇 ](https://blog.csdn.net/huan447882949/article/details/76100155/)
>
> 在宏定义里， ## 被称为*连接符（concatenator）* ， a##b 表示将ab连接起来
>
> #a 表示把a转换成字符串，即加双引号， 

所以LONAD_CONST这个指领根据宏定义展开如下:

```c
case TARGET(LOAD_CONST): {
    PRED_LOAD_CONST:
    PyObject *value = GETITEM(consts, oparg); // 获取一个PyObject* 指针对象
    Py_INCREF(value);  // 引用计数加1
    PUSH(value);     // 把刚刚创建的PyObject* push到当前的frame的stack上, 以便下一个指令从这个 stack 上面获取
    goto fast_next_opcode;
```

参考: [python 源码分析 基本篇](https://blog.csdn.net/qq_31720329/article/details/86751412)

