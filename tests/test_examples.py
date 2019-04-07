# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from attributes.examples import (
    info
)

@info('name', 'boy')
@info('age', 12)
class CS:
    pass

def test_info_get_value():
    assert info.get_value(CS, 'name') == 'boy'

def test_info_get_all():
    infos = info.get_all(CS)
    assert len(infos) == 2
    assert tuple(i.name for i in infos) == ('age', 'name')

def test_info_get_all_as_dict():
    infos = info.get_all_as_dict(CS)
    assert isinstance(infos, dict)
    assert infos['name'] == 'boy'
