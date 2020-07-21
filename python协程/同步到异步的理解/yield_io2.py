#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'

"""
在yield_io版本中，虽然实现了同步代码的异步调用，
但是在main函数中调用方式改变了，需要先执行生成器next触发生成器
def main():
    global gen
    gen = req_a()
    next(gen)
    req_b()

使用装饰器来实现 生成器的执行和唤醒，并在装饰器中开线程执行耗时操作
到这里就可以理解tornado中协程的调度的大致原理
"""


import time
import threading
from functools import wraps



def long_io():
    print()
    print('开始执行耗时操作')
    time.sleep(5)
    print('完成执行耗时操作')
    result = 'io result'
    yield result


def coroutine(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        gen = f(*args, **kwargs)
        print('当前线程id:', threading.get_ident())
        print('此时的gen_id', id(gen))
        gen_long_io = next(gen)
        def func():
            print('当前线程id:', threading.get_ident())
            print('此时的gen_id', id(gen))
            ret = next(gen_long_io)
            try:
                print('执行send操作唤醒生成器')
                gen.send(ret)
            except StopIteration:
                pass

        threading._start_new_thread(func, ())

    return wrapper


@coroutine
def req_a():
    print('开始处理请求a')
    res = yield long_io()
    print(res)
    print('完成请求处理a')


def req_b():
    print('开始处理请求b')
    time.sleep(1)
    print('完成请求处理b')


def main():
    req_a()
    req_b()

    while 1:
        pass


if __name__ == '__main__':
    main()