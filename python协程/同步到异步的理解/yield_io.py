#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'

"""
在asycn_io 异步处理的实现上，可以看到，请求逻辑和回调逻辑是要分开的，
那有没有什么机制可以不分开，，将代码写在一起，看起来是同步的，但其实是异步的

使用yield关键字, 可以将函数变成生成器，使用next(gen)调用执行, gen.send()进行唤醒

"""

import time
import threading

gen = None

def long_io():
    def func():
        global gen
        print()
        print('开始执行耗时操作')
        time.sleep(5)
        print('完成执行耗时操作')
        result = 'io result'
        try:
            print('执行send操作唤醒生成器')
            gen.send(result)
        except StopIteration:
            pass

    threading._start_new_thread(func, ())


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
    global gen
    gen = req_a()
    next(gen)
    req_b()

    while 1:
        pass


if __name__ == '__main__':
    main()