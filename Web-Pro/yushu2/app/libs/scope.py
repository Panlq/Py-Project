#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'


class BaseScope:
    level = 0
    allow_api = []   # 允许访问的api
    allow_module = []  # 允许访问的模块
    forbidden = []   # 排除法

    def __add__(self, other):
        # 运算符重载
        self.allow_api = self._set(self.allow_api + other.allow_api)
        self.allow_module = self._set(self.allow_module + other.allow_module)
        self.forbidden = self._set(self.forbidden + other.forbidden)
        return self

    def _set(self, ary):
        if not ary:
            return ary
        return list(set(ary))


class AdminScope(BaseScope):
    level = 9999
    # allow_api = []
    allow_module = ['v1.user']


class UserScope(BaseScope):
    level = 1
    allow_api = []
    forbidden = ['v1.user+super_get_user', 'v1.user+super_del_user']

    def __init__(self):
        # UserScope带有超级用户的，结合排除法
        self + AdminScope()


str2obj = {}
level2str = {}


def iteritems(d, *args, **kwargs):
    return iter(d.items(*args, **kwargs))


def _find_scope_group():
    for _name, obj in iteritems(globals()):
        try:
            is_scope_obj = issubclass(obj, BaseScope)
        except TypeError:
            is_scope_obj = False
        if not is_scope_obj or obj.level < 1:
            continue

        old_obj = str2obj.get(_name, None)
        if old_obj is not None and issubclass(obj, old_obj):
            continue
        str2obj[_name] = obj
        level2str[obj.level] = _name


# 模仿flask exceptions 预加载各个异常类的方式，将用户组自动加在如内存
_find_scope_group()
del _find_scope_group


def is_in_scope(scope, endpoint):
    # scope是字符串  使用globals() 方式不好，会把全局的变量都加在进去，太多无用
    scope = str2obj[scope]()
    md, _ = endpoint.split('+')
    if endpoint in scope.forbidden:
        return False
    if endpoint in scope.allow_api:
        return True
    if md in scope.allow_module:
        return True

    return False



