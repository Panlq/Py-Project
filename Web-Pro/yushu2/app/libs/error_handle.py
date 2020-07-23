
#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'


from werkzeug.exceptions import HTTPException

from app.libs.error import APIException
from app.libs.error_code import *


class Success(APIException):
    code = 201
    msg = 'OK'
    error_code = REQUEST_SUC


class DeleteSuccess(Success):
    code = 202
    error_code = REQUEST_FAIL


class ServerError(APIException):
    code = 500
    msg = 'sorry, we made a mistake .'
    error_code = SERVER_ERROR


class ClientTypeError(APIException):
    code = 400
    msg = 'clients is invalid'
    error_code = CLIENTTYPE_ERROR


class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = PARAMETER_EXC


class NotFound(APIException):
    code = 404
    msg = 'the resource are not found o_o'
    error_code = NOT_FOUND


class AuthFailed(APIException):
    code = 401
    msg = 'not auth'
    error_code = AUTH_FAILED




