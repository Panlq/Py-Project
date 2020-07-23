#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'

from flask import jsonify, g

from app.libs.redprint import RedPrint
from app.libs.auths import auth
from app.models.user import User

api = RedPrint('user')


@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def super_get_user(uid):
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


@api.route('', methods=['GET'])
@auth.login_required
def get_user():
    uid = g.user.uid
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)