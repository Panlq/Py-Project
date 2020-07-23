#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'

from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp
from wtforms import ValidationError

from app.models.user import User
from app.libs.enums import ClientTypeEnum
from app.validators.base import BaseForm as Form


class ClientForm(Form):
    account = StringField(validators=[DataRequired(message='不允许为空'), 
                        length(min=5, max=32)])

    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except Exception as e:
            raise e
            
        self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[
        Email(message='invalidate email')
    ])

    secret = StringField(validators=[
        DataRequired(),
        # password can only include letter, numbers, and "_"
        Regexp(r'^[A-Za-z0-9_]{6,25}$')
    ])

    nickname = StringField(validators=[
        DataRequired(),
        length(min=2, max=22)
    ])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()