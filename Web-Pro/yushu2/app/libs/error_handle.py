
#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'


from werkzeug.exceptions import HTTPException

from app.libs.error import APIException
from app.libs.error_code import *


class Success(APIException):
    code = 201   # Created
    msg = 'OK'
    error_code = REQUEST_SUC


class DeleteSuccess(Success):
    code = 202   # 204 表示删除成功 不返回内容NO CONTENT，为了保持统一，所以使用202
    error_code = REQUEST_FAIL


class ServerError(APIException):
    code = 500
    msg = 'sorry, we made a mistake .'
    error_code = SERVER_ERROR


class ClientTypeError(APIException):
    code = 400  # Bad Request
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


class MethodNotAllowed(APIException):
    code = 405   # Method Not Allowed
    msg = 'the request method is not allowed o_o'
    error_code = NOT_FOUND


class AuthFailed(APIException):
    code = 401   # 授权失败 Unauthorized
    msg = 'not auth'
    error_code = AUTH_FAILED


class Forbidden(APIException):
    code = 403   # 无权限访问
    msg = 'not auth'
    error_code = AUTH_FAILED




