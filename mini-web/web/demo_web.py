#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'


import os
import re
import time
from urllib.parse import unquote
from functools import wraps


templates_root = './static'

# 添加路由映射
"""
# url_route = {
#   "/index.py": index_func,
#   "/center.py": center_func
# }
"""

g_url_maps = dict()

def route(url):
    def wrapper(func):
        # 调用路由解析
        g_url_maps[url] = func
        @wraps(func)
        def inner_wrap(file_name):
            return func(file_name)

        return inner_wrap
    return wrapper


@route('/getpid')
def index():
    return f'<h1>PID: {time.time()}</h1>'


@route('/user')
def user():
    return 'Hello world form a simple WSGI application!--> %s \n' % time.ctime()


def parse_path(path):
    """路由解析
    学习flask怎么做路由匹配的
    """
    pass


def application(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html')]
    start_response(status, response_headers)
    path = environ['PATH_INFO']
    try:
        for url, call_func in g_url_maps.items():
            print(url)
            ret = re.match(url, path)
            if ret:
                return call_func()
        else:
            return '404 not found'

    except Exception as e:
        return '%s' % e
    else:
        return str(environ)
