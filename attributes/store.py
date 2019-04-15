# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import weakref
weakref.WeakKeyDictionary

_ATTRS = weakref.WeakKeyDictionary()
_FUNC_PARAM_DICT_WEAK = weakref.WeakKeyDictionary()
_FUNC_PARAM_DICT = {}

_ATTRS_NAME = '__cologler.attributes__'
_FUNC_PARAM_DICT_NAME = '__cologler.attributes.params__'

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

def _get_value(obj, attr_key: str, fallback_dict: dict, factory):
    ret = _get_attr(obj, attr_key) or fallback_dict.get(obj)
    if ret is None and factory is not None:
        ret = factory()
        try:
            setattr(obj, attr_key, ret)
        except (TypeError, AttributeError):
            fallback_dict[obj] = ret
    return ret

def get_attrs_list(obj, factory=None):
    '''
    gets attrs list from `obj`.

    if `factory` is not `None`, use factory create default instance.
    '''
    ret = _get_attr(obj, _ATTRS_NAME) or _ATTRS.get(obj)
    if ret is None and factory is not None:
        ret = factory()
        _set_attr(obj, _ATTRS_NAME, ret) or _set_dict(_ATTRS, obj, ret)
    return ret

def get_func_param_dict(func):
    ret = _get_attr(func, _FUNC_PARAM_DICT_NAME) or \
          _get_dict(_FUNC_PARAM_DICT, func) or \
          _get_dict(_FUNC_PARAM_DICT_WEAK, func)
    if ret is None:
        ret = {}
        assert _set_attr(func, _FUNC_PARAM_DICT_NAME, ret) or \
               _set_dict(_FUNC_PARAM_DICT_WEAK, func, ret) or \
               _set_dict(_FUNC_PARAM_DICT, func, ret)
    return ret
