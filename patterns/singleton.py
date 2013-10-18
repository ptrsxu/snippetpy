#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Singleton(object):
    """ all subclass of Singleton will be a singleton, no necessary for rewriting __new__ """
    def __new__(cls, *args, **kwargs):
        if '_inst' not in vars(cls):
            cls._inst = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._inst

class Borg(object):
    """ similar behavior of Singleton """
    _shared_state = {}
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        return obj
