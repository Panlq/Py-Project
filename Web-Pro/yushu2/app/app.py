#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'

from datetime import date
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder

from app.libs.error_handle import ServerError


class JSONEncoder(_JSONEncoder):
    """
    重写json序列化， 让User 等实例对象可序列化
    """
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        # 教程返回的是ServerError 有问题
        super(JSONEncoder, self).default(o)


class Flask(_Flask):
    json_encoder = JSONEncoder
