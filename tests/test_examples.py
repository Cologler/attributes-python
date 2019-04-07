# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from attributes.examples import (
    info
)

def test_info():
    @info('name', 'boy')
    @info('age', 12)
    class CS:
        pass

    assert info.get_value(CS, 'name') == 'boy'

    infos = info.get_all(CS)
    assert len(infos) == 2
    assert tuple(i.name for i in infos) == ('age', 'name')
