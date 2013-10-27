#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import inspect

class SuperMixin(object):
    """A way to use super.

    Example:
    >>> class Base(list, SuperMixin):
    ...     pass
    ...
    >>> class DerivedA(Base):
    ...     def dmethod(self):
    ...         print('in DerivedA')
    ...         DerivedA.super()
    ...
    >>> class DerivedB(Base):
    ...     def dmethod(self):
    ...         print('in DerivedB')
    ...         DerivedB.super()
    ...
    >>> class DDerived(DerivedA, DerivedB):
    ...     def dmethod(self):
    ...         print('in DDerived')
    ...         DDerived.super()
    ...
    >>> DDerived().dmethod()
    in DDerived
    in DerivedA
    in DerivedB
    """
    def super(cls, *args, **kwargs):
        frame = inspect.currentframe(1)
        self = frame.f_locals['self']
        method_name = frame.f_code.co_name
        method = getattr(super(cls, self), method_name, None)
        if inspect.ismethod(method):
            return method(*args, **kwargs)
    super = classmethod(super)
