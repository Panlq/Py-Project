#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'


from flask import Flask
from app.api.v1 import init_blueprint_v1


def register_blueprint(app):
    app.register_blueprint(init_blueprint_v1(), ure_prefix='/v1')



def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')
    return app