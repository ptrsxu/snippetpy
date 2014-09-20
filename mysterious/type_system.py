#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
from python cookbook 3nd edition.
"""


class Descriptor:
    """通过描述符来控制对应实例中的数据"""
    def __init__(self, name=None, **kwargs):
        self.name = name
        if kwargs:
            for k, v in kwargs.items():
                setattr(self, k, v)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class Typed(Descriptor):
    """对描述符存储的数据进行类型检查"""
    expected = (type(None), )

    def __set__(self, instance, value):
        if not type(value) in self.expected:
            raise TypeError("Type should only be: %s" % str(self.expected))
        super().__set__(instance, value)


class Integer(Typed):
    expected = (int, )


class String(Typed):
    expected = (str, )


class MaxSized(Descriptor):
    def __init__(self, name=None, **kwargs):
        if 'size' not in kwargs:
            raise TypeError("missing size option")
        super().__init__(name, **kwargs)

    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError("too long: %s" % str(value))
        super().__set__(instance, value)


class SizedString(String, MaxSized):
    pass


class User:

    """
    >>> usera = User('Peter', 9547)
    >>> usera.name
    'Peter'
    >>> usera.id
    9547
    >>> userb = User('Peter'*3, 9548)
    Traceback (most recent call last):
        ...
    ValueError: too long: PeterPeterPeter
    """
    username = MaxSized(name="name", size=10)
    identifier = Integer(name="id")

    def __init__(self, username, identifier):
        self.username = username
        self.identifier = identifier
