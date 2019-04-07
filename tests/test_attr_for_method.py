# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from pytest import raises

from attributes import Attribute

class UnUsed(Attribute):
    pass

class Data(Attribute):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

class SomeClass:
    @Data('method')
    def method(self):
        pass

    @classmethod
    @Data('cmethod')
    def cmethod(cls):
        pass

    @staticmethod
    @Data('smethod')
    def smethod():
        pass

class SomeClassSub(SomeClass):
    def method(self):
        pass

    @classmethod
    def cmethod(cls):
        pass

    @staticmethod
    def smethod():
        pass

def test_method_get_attrs():
    for method in (SomeClass.method, SomeClass().method):
        attrs = Attribute.get_attrs(method)
        attr, = attrs
        assert attr.args == ('method', )

    for method in (SomeClassSub.method, SomeClassSub().method):
        attrs = Attribute.get_attrs(method)
        assert not attrs

def test_class_method_get_attrs():
    for method in (SomeClass.cmethod, SomeClass().cmethod):
        attrs = Attribute.get_attrs(method)
        attr, = attrs
        assert attr.args == ('cmethod', )

def test_static_method_get_attrs():
    for method in (SomeClass.smethod, SomeClass().smethod):
        attrs = Attribute.get_attrs(method)
        attr, = attrs
        assert attr.args == ('smethod', )

def test_methods_not_inherit():
    for method in (
        SomeClassSub.method, SomeClassSub().method,
        SomeClassSub.cmethod, SomeClassSub().cmethod,
        SomeClassSub.smethod, SomeClassSub().smethod,
    ):
        assert not Attribute.get_attrs(method)
        assert not Attribute.get_attrs(method, inherit=True)
