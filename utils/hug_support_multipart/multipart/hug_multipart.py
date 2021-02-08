#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021/2/3 20:20
# @Author   : Jonpan
# @File     : hug_multipart.py
# @Software : VsCoe
# @Desc     :

from hug.format import content_type

from .multipart import MultipartParser


@content_type("multipart/form-data")
def multipart(body, content_length=0, **header_params):
    """
    Converts multipart form data into native Python objects

    """

    header_params.setdefault("CONTENT-LENGTH", content_length)
    if header_params and "boundary" in header_params:
        if type(header_params["boundary"]) is str:
            header_params["boundary"] = header_params["boundary"].encode()

    parser = MultipartParser(stream=body, boundary=header_params["boundary"])
    form = dict(
        zip(
            [p.name for p in parser.parts()],
            [
                FileLikeObject(p.filename, p) if p.filename else p.file.read().decode()
                for p in parser.parts()
            ],
        )
    )

    return form


class FileLikeObject(object):
    def __init__(self, filename, obj):
        self.filename = filename
        self.multipart = obj
        self.file = self.multipart.file
        self.read = self.file.read

    @property
    def name(self):
        return self.filename

    def __get__(self, key):
        return self.__dict__.get(key)

    def __len__(self):
        return self.size

    @property
    def size(self):
        return self.file.__sizeof__()
