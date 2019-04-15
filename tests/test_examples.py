# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from attributes.examples import (
    info, props
)

def test_info_get_value():
    @info('name', 'eva')
    class Person: pass
    assert info.get_value(Person, 'name') == 'eva'

def test_info_get_all():
    @info('name', 'eva')
    @info('age', 12)
    class Person: pass
    infos = info.get_from(Person)
    assert tuple(i.name for i in infos) == ('name', 'age', )

def test_info_get_as_dict():
    @info('name', 'eva')
    @info('age', 12)
    class Person: pass
    infos = info.get_as_dict(Person)
    assert isinstance(infos, dict)
    assert infos['name'] == 'eva'

def test_info_get_as_dict_override():
    @info('name', 'eva')
    @info('name', 'john')
    class Person: pass
    infos = info.get_as_dict(Person)
    assert isinstance(infos, dict)
    assert infos['name'] == 'eva'

def test_info_doc_examples():
    @info('name', 'eva')
    class Person: pass
    assert info.get_value(Person, 'name') == 'eva'

def test_props_get_as_dict_inherit():
    @props(age=12, name='no-name')
    class Animal: pass
    @props(name='eva')
    class Person(Animal): pass
    assert props.get_as_dict(Person, inherit=True) == {
        'name': 'eva',
        'age': 12
    }

def test_props_doc_examples():
    @props(name='eva')
    class Person: pass
    assert props.get_as_dict(Person)['name'] == 'eva'
