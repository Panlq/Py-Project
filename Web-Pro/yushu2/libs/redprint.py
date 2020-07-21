#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'



class RedPrint(object):
    def __init__(self, name):
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        def decorator(f):
            self.mound.append((f, rule, options))
            return f
        
        return decorator

    def register(self, bp, url_prefix=None):
        # 视图函数向蓝图注册  原本蓝图实在注册的时候就进行url绑定
        if url_prefix == None:
            url_prefix = '/' + self.name
        for f, rule, options in self.mound:
            endpoint = options.pop('endpoint', f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)