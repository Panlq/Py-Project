#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'


from flask import request
from wtforms import Form

from app.libs.error_handle import ParameterException


class BaseForm(Form):
    """
    由于From表单在validate的时候并不会抛出异常而是将异常信息放在errors参数中，
    所以在此继承Form写一个自动校验并抛出异常的方法
    """

    def __init__(self):
        # 当body中没有数据的时候且 header中
        # contentType: application/json的时候request.json获取不到会报错
        # 使用以下方式不会报错
        data = request.get_json(silent=True)
        kwargs = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **kwargs)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise ParameterException(msg=self.errors)

        return self
