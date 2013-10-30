#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
A colleciton of snippet for python code about advanced feature descriptors.
"""

class DefaultAlias(object):
    """An Alias name of an attribute in another class."""
    def __init__(self, name):
        self.name = name

    def __get__(self, inst, cls):
        if inst is None:
            return self
        return getattr(inst, self.name)


class Alias(DefaultAlias):

    def __set__(self, inst, value):
        setattr(inst, self.name, value)

    def __delete__(self, inst):
        delattr(inst, self.name)


import warnings
class OldAlias(Alias):
    """An Alias name(used before) of an attribute in another class.

    We can use OldAlias to define an attribute which is used before but
    no longer recommended. When we use the old attribute, it would
    automatically point to the new one. The example will print:

        __main__:1: DeprecationWarning: use'good' instead of 'bad'.

    if running python with ``python -Wall`` .

    Example:
    >>> class Nice(object):
    ...     def __init__(self, name):
    ...         self.new_name = name
    ...     old_name = OldAlias('new_name', 'old_name')
    ...
    >>> x = Nice('peter')
    >>> x.old_name
    'peter'
    >>> x.old_name = 'jacky'
    >>> x.new_name
    'jacky'
    """
    def _warn(self):
        warnings.warn('use %r instead of %r.' % (self.name, self.oldname),
               DeprecationWarning, stacklevel=3)

    def __init__(self, name, oldname):
        super(OldAlias, self).__init__(name)
        self.oldname = oldname

    def __get__(self, inst, cls):
        self._warn()
        return super(OldAlias, self).__get__(inst, cls)

    def __set__(self, inst, value):
        self._warn()
        return super(OldAlias, self).__set__(inst, value)

    def __delete__(self, inst):
        self._warn()
        return super(OldAlias, self).__delete__(inst)
