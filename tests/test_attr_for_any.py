# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from pytest import raises

from attributes import Attribute

class Data(Attribute):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

def test_for_unhashable():
    class A:
        def __eq__(self):
            raise NotImplementedError

    a = A()

    with raises(TypeError, match='unhashable type'):
        hash(a)

    Data(a=15)(a)
    data = Data.get_first_from(a)
    assert data.kwargs == {'a': 15}
