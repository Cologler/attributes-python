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

def test_paramof_is_singleton():
    from attributes.core import param_of

    def func():
        pass
    assert param_of(func, 'a') is param_of(func, 'a')


def test_param_attr_get():
    @param_attr('a', Data(1, 2))
    def func(a, b):
        pass

    attrs = Data.get_from_param(func, 'a')
    assert len(attrs) == 1
    data = attrs[0]
    assert data.args == (1, 2)

def test_param_attr_hide_in_func_attrs():
    @param_attr('a', Data('func:a-attr'))
    @Data('func-attr')
    def func(a, b):
        pass

    attrs = Data.get_from_param(func, 'a')
    assert len(attrs) == 1
    data = attrs[0]
    assert data.args == ('func:a-attr', )

    attrs = Data.get_from(func)
    assert len(attrs) == 1
    data = attrs[0]
    assert data.args == ('func-attr', )
