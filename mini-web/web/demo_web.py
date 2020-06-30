#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'


import time


def application(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html')]
    start_response(status, response_headers)
    return str(environ) + '\n==Hello world form a simple WSGI application!--> %s \n' % time.ctime()
