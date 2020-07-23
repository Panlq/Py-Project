#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'

from collections import namedtuple
from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,\
                        BadSignature, SignatureExpired

from app.libs.error_handle import AuthFailed, Forbidden
from app.libs.error_code import TOKEN_EXPIRED, TOKEN_INVALID
from app.libs.scope import is_in_scope


User = namedtuple('User', ['uid', 'ac_type', 'scope'])
auth = HTTPBasicAuth()


class CryptoMgr:

    @staticmethod
    def gen_serialzer(expiration=None):
        if not expiration:
            expiration = current_app.config['TOKEN_EXPIRATION']
        return Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)

    @staticmethod
    def generate_token(uid, ac_type, scope=None, expiration=None):
        s = CryptoMgr.gen_serialzer(expiration)
        token = s.dumps({
            'uid': uid,
            'type': ac_type,
            'scope': scope
        })
        return token.decode('utf8')

    @staticmethod
    def decrypt_token(token):
        s = CryptoMgr.gen_serialzer()
        try:
            data = s.loads(token)
        except BadSignature:
            raise AuthFailed(msg='token is invalid', error_code=TOKEN_INVALID)
        except SignatureExpired:
            raise AuthFailed(msg='token is expired', error_code=TOKEN_EXPIRED)

        uid = data['uid']
        ac_type = data['type']
        scope = data['scope']

        return User(uid, ac_type, scope)


@auth.verify_password
def verify_auth(token, p):
    # token
    user_info = CryptoMgr.decrypt_token(token)
    if not user_info:
        return False
    else:
        check_access(user_info.scope)
        g.user = user_info
        return True


def check_access(scope: 'str'):
    # 检测访问权限，是否越级访问
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()
