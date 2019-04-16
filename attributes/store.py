# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import weakref
weakref.WeakKeyDictionary

_ATTRS_WEAK = weakref.WeakKeyDictionary()
_ATTRS = {}

_ATTRS_NAME = '__cologler.attributes__'

def _get_attr(obj, k):
    try:
        d = vars(obj)
    except TypeError:
        # donot have __dict__
        return None
    return d.get(k)

def _set_attr(obj, attr_name, v) -> bool:
    try:
        setattr(obj, attr_name, v)
        return True
    except (TypeError, AttributeError):
        return False

def _get_dict(d, k):
    try:
        return d.get(k)
    except TypeError:
        # cannot create weak reference
        pass

def _set_dict(d, k, v) -> bool:
    try:
        d[k] = v
        return True
    except TypeError:
        # cannot create weak reference
        return False

class AttrsList(list):
    paramsdict: dict=None

    def __bool__(self):
        # so we can use `_get_attr` and `_get_dict` chain without recreate new instance.
        return True


def get_attrs_list(obj):
    '''
    gets attrs list from `obj`, return `None` if not created.
    '''
    return _get_attr(obj, _ATTRS_NAME) or _get_dict(_ATTRS_WEAK, obj) or _get_dict(_ATTRS, obj)

def get_or_create_attrs_list(obj):
    '''
    get or create attrs list from `obj`.
    '''
    ret = get_attrs_list(obj)
    if ret is None:
        ret = AttrsList()
        assert _set_attr(obj, _ATTRS_NAME, ret) or \
               _set_dict(_ATTRS_WEAK, obj, ret) or \
               _set_dict(_ATTRS, obj, ret)
    return ret

def get_func_param_dict(func):
    attrs_list = get_or_create_attrs_list(func)
    if attrs_list.paramsdict is None:
        attrs_list.paramsdict = {}
    return attrs_list.paramsdict
