#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'

from flask import current_app, jsonify

from app.models.user import User
from app.libs.redprint import RedPrint
from app.libs.enums import ClientTypeEnum
from app.libs.error_handle import AuthFailed
from app.validators.forms import ClientForm
from app.libs.auths import CryptoMgr


api = RedPrint('token')


@api.route('', methods=['POST'])
def get_token():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify,
    }
    # gen_token
    expiration = current_app.config['TOKEN_EXPIRATION']
    identiry = promise[form.type.data](form.account.data, form.secret.data)
    token = CryptoMgr.generate_token(identiry['uid'],
                                     form.type.data.value,
                                     identiry['scope'],
                                     expiration)

    return jsonify({'token': token}),  201


