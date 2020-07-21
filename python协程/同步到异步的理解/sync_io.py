#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'


# 模拟同步io执行过程

import time

def long_io():
    print('开始执行耗时操作')
    time.sleep(5)
    print('完成执行耗时操作')
    result = 'io result'
    return result


def req_a():
    print('开始处理请求a')
    res = long_io()
    print(res)
    print('完成请求处理a')


def req_b():
    print('开始处理请求b')
    print('完成请求处理b')


def main():
    req_a()
    req_b()


if __name__ == '__main__':
    main()