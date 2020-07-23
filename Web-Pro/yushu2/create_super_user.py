#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'


from app import create_app
from app.models.base import db
from app.models.user import User

app = create_app()


def create_super_user():
    with app.app_context():
        with db.auto_commit():
            user = User()
            user.nickname = 'super'
            user.password = '123456'
            user.email = '9999@163.com'
            user.auth = 9999
            db.session.add(user)


if __name__ == '__main__':
    create_super_user()
