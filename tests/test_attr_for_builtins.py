# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from attributes import Attribute, param_attr

class Data(Attribute):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

def test_str():
    Data()(str)

    assert len(Data.get_from(str)) == 1

def test_int():
    Data()(int)

    assert len(Data.get_from(int)) == 1

def test_bool():
    Data()(bool)

    assert len(Data.get_from(bool)) == 1

def test_str_method():
    param_attr('self', Data())(str.join)

    assert len(Data.get_from_param(str.join, 'self')) == 1

