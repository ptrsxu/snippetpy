#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Proxy(object):
    """Base of all Proxy classes."""
    def __init__(self, obj):
        super(Proxy, self).__init__()
        self._obj = obj

    # all non-special method can be auto delegated.
    # for example: list.append
    def __getattr__(self, attr):
        return getattr(self._obj, attr)

def make_binder(unbounded_method):
    def f(self, *args, **kwargs):
        return unbounded_method(self._obj, *args, **kwargs)
    f.__name__ = unbounded_method.__name__
    return f

known_proxy_classes = {}

def proxy(obj, *specials):
    """Factory function that can delegate special functions to an obj.

    Example:
    >>> o = proxy([], 'len', 'iter')
    >>> type(o)
    <class 'proxy.listProxy'>
    >>> o.append(3)
    >>> o.append(5)
    >>> len(o)
    2
    >>> try:
    ...    o[0]
    ... except TypeError:
    ...    print('error becuase __getitem__ not delegated.')
    ...
    error becuase __getitem__ not delegated.
    """
    obj_cls = obj.__class__
    key = obj_cls, specials
    cls = known_proxy_classes.get(key)
    if cls is None:
        cls = type('%sProxy' % obj_cls.__name__, (Proxy,), {})
        for name in specials:
            name = '__%s__' % name
            unbounded_method = getattr(obj_cls, name)
            setattr(cls, name, make_binder(unbounded_method))
        known_proxy_classes[key] = cls
    return cls(obj)
