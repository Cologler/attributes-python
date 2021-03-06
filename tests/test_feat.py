# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from pytest import raises

from attributes import Attribute

def test_should_be_new_instance_everytime():
    class Data(Attribute):
        def __init__(self, f, s):
            self.f = f
            self.s = s

    @Data(1, 2)
    class SomeClass:
        pass

    attrs_1 = Attribute.get_attrs(SomeClass)
    assert len(attrs_1) == 1
    attrs_2 = Attribute.get_attrs(SomeClass)
    assert len(attrs_2) == 1
    assert attrs_1[0] is not attrs_2[0]

def test_allow_multiple():
    class Data(Attribute):
        def __init__(self, *args):
            self.value = args

    @Data(1, 2)
    @Data(3, 4)
    class SomeClass:
        pass

    attrs = Attribute.get_attrs(SomeClass)
    assert len(attrs) == 2
    a1, a2 = attrs
    assert a1.value == (1, 2)
    assert a2.value == (3, 4)

def test_allow_multiple_inherit_behavior():
    class Default(Attribute):
        pass

    assert Default.allow_multiple

    class AllowMultiple(Attribute, allow_multiple=True):
        pass

    assert AllowMultiple.allow_multiple

    class NotAllowMultiple(Attribute, allow_multiple=False):
        pass

    assert not NotAllowMultiple.allow_multiple

    with raises(ValueError):
        class CannotBeAllowMultiAgain(NotAllowMultiple, allow_multiple=True):
            pass

def test_not_allow_multiple():
    class Data(Attribute, allow_multiple=False):
        pass

    with raises(SyntaxError):
        @Data()
        @Data()
        class SomeClass:
            pass

def test_not_allow_multiple_with_inherit():
    class Data(Attribute, allow_multiple=False):
        pass

    class SubData(Data):
        pass

    with raises(SyntaxError):
        @SubData()
        @SubData()
        class SomeClass:
            pass

    with raises(SyntaxError):
        @Data()
        @SubData()
        class SomeClass:
            pass

    with raises(ValueError):
        class SubData_2(Data, allow_multiple=True):
            pass

def test_on_attach():
    class PubFunc(Attribute):
        items = []
        @classmethod
        def on_attach(cls, target):
            cls.items.append(target)

    @PubFunc()
    def func():
        pass

    assert PubFunc.items == [func]
