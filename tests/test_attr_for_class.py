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

@Data(1, 2)
class SomeClass:
    pass

class SomeClassSub(SomeClass):
    pass

def test_get_attrs():
    attrs = Attribute.get_attrs(SomeClass)
    attr, = attrs
    assert attr.args == (1, 2)

def test_get_attrs_order():
    @Data(2)
    @Data(1)
    class Kls:
        pass

    attrs = Attribute.get_attrs(Kls)
    assert tuple(a.args[0] for a in attrs) == (2, 1)

def test_get_attrs_by_inherit():
    attrs = Attribute.get_attrs(SomeClassSub)
    assert len(attrs) == 0
    attrs = Attribute.get_attrs(SomeClassSub, inherit=True)
    assert len(attrs) == 1

def test_get_attrs_order_by_inherit():
    @Data(3)
    class C1:
        pass

    @Data(2)
    class C2(C1):
        pass

    @Data(1)
    class C3(C2):
        pass

    attrs = Attribute.get_attrs(C3, inherit=True)
    assert tuple(a.args[0] for a in attrs) == (1, 2, 3)

def test_get_attr():
    attr = Attribute.get_attr(SomeClass, UnUsed)
    assert attr is None
    attr = Attribute.get_attr(SomeClass, Data)
    assert attr.args == (1, 2)

def test_get_attr_by_inherit():
    attr = Attribute.get_attr(SomeClassSub, UnUsed)
    assert attr is None
    attr = Attribute.get_attr(SomeClassSub, UnUsed, inherit=True)
    assert attr is None
    attr = Attribute.get_attr(SomeClassSub, Data)
    assert attr is None
    attr = Attribute.get_attr(SomeClassSub, Data, inherit=True)
    assert attr is not None

def test_get_inherited_attr():
    class Parent(Attribute):
        pass
    class Current(Parent):
        pass
    class Sub(Current):
        pass

    @Current()
    class SomeClassScoped:
        pass

    attr = Attribute.get_attr(SomeClassScoped, Parent)
    assert attr is not None
    attr = Attribute.get_attr(SomeClassScoped, Current)
    assert attr is not None
    attr = Attribute.get_attr(SomeClassScoped, Sub)
    assert attr is None

def test_has_attr():
    assert not Attribute.has_attr(SomeClass, UnUsed)
    assert Attribute.has_attr(SomeClass, Data)

def test_attr_origin_target():
    attr = Attribute.get_attr(SomeClassSub, Data, inherit=True)
    assert attr.origin_target is SomeClass

def test_attr_target():
    attr = Attribute.get_attr(SomeClassSub, Data, inherit=True)
    assert attr.target is SomeClassSub

def test_attr_init_targets():
    class RequiredError(Exception):
        pass

    class SomeAttr(Attribute):
        def __init__(self):
            assert self.target is SomeClassExample
            assert self.origin_target is SomeClassExample
            raise RequiredError

    @SomeAttr()
    class SomeClassExample:
        pass

    with raises(RequiredError):
        SomeAttr.get_attr(SomeClassExample, SomeAttr)
