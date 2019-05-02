# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import threading
import weakref

_ATTRS_WEAK = weakref.WeakKeyDictionary()
_ATTRS = {}
_ATTRS_LIST = []
_LOCK = threading.Lock()

_ATTRS_NAME = '__cologler.attributes__'

def _is_hashable(obj) -> bool:
    try:
        hash(obj)
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
    # get from type
    # unable to use `getattr` because of
    # `getattr` will get attr from parent class
    try:
        d = vars(obj)
    except TypeError:
        # donot have __dict__
        d = None

    if d is not None:
        try:
            return d[_ATTRS_NAME]
        except KeyError:
            pass

    if _is_hashable(obj):
        # get from weak dict
        try:
            return _ATTRS_WEAK[obj]
        except (TypeError, KeyError):
            # TypeError: cannot create weak reference
            pass

        # get from dict
        try:
            return _ATTRS[obj]
        except KeyError:
            pass

    else:
        for item in _ATTRS_LIST:
            if item[0] is obj:
                return item[1]

    return None

def _set_attrs_list(obj, attrlist):
    try:
        setattr(obj, _ATTRS_NAME, attrlist)
        return
    except (TypeError, AttributeError):
        pass

    if _is_hashable(obj):
        try:
            _ATTRS_WEAK[obj] = attrlist
            return
        except TypeError:
            # cannot create weak reference
            pass

        _ATTRS[obj] = attrlist

    else:
        _ATTRS_LIST.append((obj, attrlist))


def get_or_create_attrs_list(obj):
    '''
    get or create attrs list from `obj`.
    '''
    attrs_list = get_attrs_list(obj)
    if attrs_list is None:
        with _LOCK:
            attrs_list = get_attrs_list(obj)
            if attrs_list is None:
                attrs_list = AttrsList()
                _set_attrs_list(obj, attrs_list)

    return attrs_list

def get_func_param_dict(func):
    attrs_list = get_or_create_attrs_list(func)
    if attrs_list.paramsdict is None:
        attrs_list.paramsdict = {}
    return attrs_list.paramsdict
