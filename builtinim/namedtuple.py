#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
from python cookbook 2nd edition.
"""

from operator import itemgetter


def named_tuple(typename, *attrs):
    """A new class that there elements can be fetched by attr names.

    Example:
    >>> Point = named_tuple('Point', 'x', 'y')
    >>> Point.__name__
    'Point'
    >>> p1 = Point(4, 1)
    >>> p2 = Point(1, 5)
    >>> print('(%s, %s)' % (p1.x, p1.y))
    (4, 1)
    >>> print('(%s, %s)' % (p2.x, p2.y))
    (1, 5)
    """

    nattrs = len(attrs)

    class _NamedTuple(tuple):
        # we donnot need to offer a dict for each instance to save
        # memory, so we use __slots__.
        __slots__ = ()

        def __new__(cls, *attrs):

            if len(attrs) != nattrs:
                raise TypeError('%s takes exactly %d args (%d given)' %
                                (typename, nattrs, len(attrs)))
            return tuple.__new__(cls, attrs)

        def __repr__(self):
            return '%s(%s)' % (typename, ', '.join(map(repr, self)))

    for i, a in enumerate(attrs):
        setattr(_NamedTuple, a, property(itemgetter(i)))
    setattr(_NamedTuple, '__name__', typename)
    # _NamedTuple.__name__ = typename

    return _NamedTuple
