#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'


# 使用线程异步执行耗时io
# 当调用long_io的时候，将long_io放入一个线程中执行, 要考虑异步执行的结果回调返回

import time
import threading


def func(callback):
    print()
    print('开始执行耗时操作')
    time.sleep(5)
    print('完成执行耗时操作')
    result = 'io result'
    callback(result)


def long_io(cb):
    threading._start_new_thread(func, (cb, ))
    

def on_finish(res):
    print('开始执行回掉函数')
    print(res)
    print('完成回掉函数执行')


def req_a():
    print('开始处理请求a')
    long_io(on_finish)
    print('离开请求处理a')


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