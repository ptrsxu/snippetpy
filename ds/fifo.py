#!/usr/bin/env python
# -*- coding: utf-8 -*-

class FIFO(list):
    """a FIFO, use append() for input and pop() for output.

    Example:
    >>> f = FIFO()
    >>> f.append(1)
    >>> f.append(9)
    >>> f.append(5)
    >>> f.pop()
    1
    """
    def __init__(self):
        self.back = []
        self.append = self.back.append
    # a O(1) pop()
    def pop(self):
        if not self:
            self.back.reverse()
            self[:] = self.back
            del self.back[:]
        return super(FIFO, self).pop()


class FIFOList(list):
    """a FIFO, use append() for input and pop() for output.

    Example:
    >>> f = FIFOList()
    >>> f.append(1)
    >>> f.append(9)
    >>> f.append(5)
    >>> f.pop()
    1
    """
    # a O(n) pop()
    def pop(self):
        return super(FIFOList, self).pop(0)


class FIFODict(dict):
    """a FIFO, based on a dict, which make the pop() cost O(1).

    Example:
    >>> f = FIFODict()
    >>> f.append(1)
    >>> f.append(9)
    >>> f.append(5)
    >>> f.pop()
    1
    """
    def __init__(self):
        self.nextin = 0
        self.nextout = 0
    def append(self, data):
        self.nextin += 1
        self[self.nextin] = data
    def pop(self):
        self.nextout += 1
        return dict.pop(self, self.nextout)


import collections
class FIFODeque(collections.deque):
    """a FIFO, based on a deque.

    Example:
    >>> f = FIFODeque()
    >>> f.append(1)
    >>> f.append(9)
    >>> f.append(5)
    >>> f.pop()
    1
    """
    pop = collections.deque.popleft


import UserDict
class FIFOCache(object, UserDict.DictMixin):
    """A map that can remember the items set.

    Example:
    >>> f = FIFOCache(num_entries=3)
    >>> f['wish'] = 'fly'
    >>> f['name'] = 'peter'
    >>> f['age'] = '3'
    >>> f['height'] = '170cm'
    >>> f.keys()
    ['name', 'age', 'height']
    """
    def __init__(self, num_entries, d=()):
        self.num_entries = num_entries
        self.d = dict(d)
        self.l = []
    def __repr__(self):
        return '%r(%r, %r)' % (self.__class__.__name__,
                self.num_entries, self.d)
    def copy(self):
        return self.__class__(self.num_entries, self.d)
    def keys(self):
        return list(self.l)
    def __getitem__(self, key):
        return self.d[key]
    def __setitem__(self, key, value):
        d = self.d
        l = self.l
        if key in d:
            l.remove(key)
        d[key] = value
        l.append(key)
        if len(l) > self.num_entries:
            del d[l.pop(0)]
    def __delitem__(self, key):
        self.d.pop(key)
        self.l.remove(key)
    def __contains__(self, item):
        return item in self.d
    has_key = __contains__


class LRUCache(FIFOCache):
    """Least Recently Used Cache."""
    def __getitem__(self, key):
        if key in self.d:
            self.l.remove(key)
        else:
            raise KeyError
        self.l.append(key)
        return self.d[key]
