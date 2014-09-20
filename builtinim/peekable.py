#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
from python cookbook 2nd edition.
"""
import collections


class Peekable(object):
    """A iteration that can look forward with normal iter operations.

    Example:
    >>> p = Peekable(iter(range(4)))
    >>> p.peek()
    0
    >>> p.next(1)
    [0]
    >>> p.peek(3)
    [1, 2, 3]
    >>> p.next(2)
    [1, 2]
    """
    def __init__(self, iterable):
        self._iterable = iterable
        self._cache = collections.deque()

    def __iter__(self):
        return self

    def _fill_cache(self, n):
        if n is None:
            n = 1
        while len(self._cache) < n:
            self._cache.append(self._iterable.next())

    def next(self, n=None):
        self._fill_cache(n)
        if n is None:
            result = self._cache.popleft()
        else:
            result = [self._cache.popleft() for i in range(n)]
        return result

    def peek(self, n=None):
        self._fill_cache(n)
        if n is None:
            result = self._cache[0]
        else:
            result = [self._cache[i] for i in range(n)]
        return result
