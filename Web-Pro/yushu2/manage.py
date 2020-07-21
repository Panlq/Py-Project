#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'

from app.app import create_app


app = create_app()


@app.route('/get')
def get_user():
    return '<h1>sdfs</h1>'


if __name__ == '__main__':
    app.run(debug=True)
    