#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'

"""
>>> import os
>>> os.urandom(24)

>>> import uuid
>>> uuid.uuid4().hex

>>> import secrets
>>> secrets.token_urlsafe(16)

>>> import binascii
>>> binascii.hexlify(os.urandom(24))
"""


SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:123456@localhost/yushu2'
# 动态追踪修改设置，如未设置只会提示警告
SQLALCHEMY_TRACK_MODIFICATIONS = True
#查询时会显示原始SQL语句
SQLALCHEMY_ECHO = True

SECRET_KEY = r'\x88D\xf09\x6\xa0A\x7\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x98*4'