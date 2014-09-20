#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
from python cookbook 2nd edition.
"""

import copy

class ChangeCheckerMixin(object):
    """Mixin class that can moniter a change of the instances' attrs.
    Just add the containers that you want to check into container_items.

    Example:
    >>> class Eg(ChangeCheckerMixin):
    ...     def __init__(self, *a, **k):
    ...         self.l = list(*a, **k)
    ...     def __str__(self):
    ...         return 'Eg(%s)' % str(self.l)
    ...     def __getattr__(self, a):
    ...         return getattr(self.l, a)
    ...
    >>> x = Eg('abcde')
    >>> print(x)
    Eg(['a', 'b', 'c', 'd', 'e'])
    >>> x.snapshot()
    >>> x.is_changed()
    False
    >>> x.append('z')
    >>> x.is_changed()
    True
    """
    container_items = {dict: dict.items, list: enumerate}
    immutable = False

    def snapshot(self):
        if self.immutable:
            return
        self._snapshot = self._copy_container(self.__dict__)

    def make_immutable(self):
        self.immutable = True
        try:
            del self._snapshot
        except AttributeError:
            pass

    def _copy_container(self, container):
        new_container = copy.copy(container)
        for k, v in self.container_items[type(new_container)](new_container):
            if type(v) in self.container_items:
                new_container[k] = self._copy_container(v)
            elif hasattr(v, 'snapshot'):
                v.snapshot()
        return new_container

    def is_changed(self):
        if self.immutable:
            return False
        snap = self.__dict__.pop('_snapshot', None)
        if snap is None:
            return True
        try:
            return self._check_container(self.__dict__, snap)
        finally:
            self._snapshot = snap

    def _check_container(self, container, snapshot):
        if len(container) != len(snapshot):
            return True
        for k, v in self.container_items[type(container)](container):
            try:
                ov = snapshot[k]
            except LookupError:
                return True
            if self._check_item(v, ov):
                return True
        return False

    def _check_item(self, newitem, olditem):
        if type(newitem) != type(olditem):
            return True
        if type(newitem) in self.container_items:
            return self._check_container(newitem, olditem)
        if newitem is olditem:
            method_is_changed = getattr(newitem, 'is_changed', None)
            if method_is_changed is None:
                return False
            return method_is_changed()
        return newitem != olditem
