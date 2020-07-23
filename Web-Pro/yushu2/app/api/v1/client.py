#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'

from app.libs.redprint import RedPrint
from app.libs.enums import ClientTypeEnum
from app.libs.error_handle import ClientTypeError, Success
from app.validators.forms import ClientForm, UserEmailForm
from app.models.user import User


api = RedPrint('client')


@api.route('/register', methods=['POST'])
def create_client():
    # 注册
    form = ClientForm().validate_for_api()
    promise(form.type.data)
    return Success()    


def promise(type_):
    options = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email
    }
    options[type_]()


def __register_user_by_email():
    form = UserEmailForm().validate_for_api()
    User.register_by_email(
        form.nickname.data,
        form.account.data,
        form.secret.data
    )