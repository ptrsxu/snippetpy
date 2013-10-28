#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect

def wrap_callable(any_callable, before, after):
    def _wrapped(*args, **kwargs):
        before()
        try:
            return any_callable(*args, **kwargs)
        finally:
            after()
    return _wrapped


class GenericWrapper(object):
    def __init__(self, obj, before, after, ignore=()):
        clsname = 'GenericWrapper'
        self.__dict__['_%s__methods' % clsname] = {}
        self.__dict__['_%s__obj' % clsname] = obj
        for name, method in inspect.getmembers(obj, inspect.ismethod):
            if name not in ignore and method not in ignore:
                self.__methods[name] = wrap_callable(method, before, after)

    def __getattr__(self, name):
        try:
            return self.__methods[name]
        except KeyError:
            return getattr(self.__obj, name)

    def __setattr__(self, name, value):
        setattr(self.__obj, name, value)


class SynchronizedObject(GenericWrapper):
    """The objects decorated by this class will be threading safe."""
    def __init__(self, obj, ignore=(), lock=None):
        if lock is None:
            import threading
            lock = threading.RLock()
        GenericWrapper.__init__(self, obj, lock.acquire, lock.release, ignore)
