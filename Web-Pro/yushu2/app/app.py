#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'


from flask import Flask, current_app
from app.api.v1 import init_blueprint_v1
from app.libs.error import APIException, HTTPException
from app.libs.error_handle import ServerError


def register_blueprint(app):
    app.register_blueprint(init_blueprint_v1(), url_prefix='/v1')


def framework_error(e):
    if isinstance(e, APIException):
        return e
    elif isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)

    else:
        if not current_app.config['DEBUG']:
            return ServerError()
        else:
            raise e


def register_plugin(app):
    from app.models.base import db
    db.init_app(app)
    db.create_all(app=app)
    # with app.app_context():
    #     db.create_all()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')
    register_blueprint(app)
    app.errorhandler(Exception)(framework_error)
    register_plugin(app)
    return app