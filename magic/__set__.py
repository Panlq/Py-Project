#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Time    :   2024/06/27 13:09:36
# @Author  :   panlq01@mingyuanyun.com
# @File    :   _set.py
# @Software:   Visual Studio Code
# @Desc    :   __set__ 魔法方法的使用，参考来源于peewee FieldAccessor


class FieldAccessor(object):
    def __init__(self, model, field, name):
        self.model = model
        self.field = field
        self.name = name

    def __get__(self, instance, instance_type=None):
        if instance is not None:
            return instance.__data__.get(self.name)
        return self.field

    def __set__(self, instance, value):
        instance.__data__[self.name] = value
        instance._dirty.add(self.name)


class Field:
    def __init__(self, **kwargs):
        self.model = None
        self.column_name = ""
        self.name = ""

    def bind(self, model, name, set_attribute: bool = False):
        self.model = model
        self.name = name
        self.column_name = self.column_name or name
        if set_attribute:
            setattr(model, name, FieldAccessor(model, self, name))


class ModelBase:
    def __init__(self):
        self.__data__ = {}
        self._dirty = set()

    def __new__(cls):
        fields = []
        for key, value in cls.__dict__.items():
            if isinstance(value, Field):
                fields.append((key, value))

        for name, field in fields:
            field.bind(cls, name, True)

        return super(ModelBase, cls).__new__(cls)


class TestModel(ModelBase):
    status = Field(column_name="status")


if __name__ == "__main__":

    t2 = TestModel()
    print(t2._dirty)
    t2.status = "finished"

    print(t2.status)

    print(t2._dirty)
