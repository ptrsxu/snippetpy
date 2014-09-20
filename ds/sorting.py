#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
from python cookbook 2nd edition.
A collection of tools for sorting and searching.
"""

import operator
import re
import heapq
from bisect import bisect_left, insort_left
import UserDict


def dict_sorted_values_by_key(d):
    ks = d.keys()
    ks.sort()
    # Another way: return map(d.get, ks)
    return [d[k] for k in ks]


def list_sort_caseinsensitive(l):
    # we can also use the above function:
    #   dci = {e.lower:e for e in l}
    #   return dict_sorted_values_by_key(dci)
    return sorted(l, key=str.lower)


def list_sort_by_attr(l, attr):
    return sorted(l, key=operator.attrgetter(attr))


def list_sort_by_attr_inplace(l, attr):
    return l.sort(key=operator.attrgetter(attr))


def embedded_integers(s):
    REGEX = r'(\d+)'
    re_digits = re.compile(REGEX)
    pieces = re_digits.split(s)
    pieces[1::2] = map(int, pieces[1::2])
    return pieces[1::2]


def list_sort_by_embedded_integers(l):
    return sorted(l, key=embedded_integers)


def isorted(data):
    data = list(data)
    heapq.heapify(data)
    while data:
        yield heapq.heappop(data)


def nsmallest(n, data):
    return heapq.nsmallest(n, data)


def qsort(l):
    """the famous quick sort algorithm.

    This is just for showing the algorithm, we should use l.sort()
    in real projects.

    Example:
    >>> l = [4, 9, 1, 6, 3, 8, 5, 10, 7]
    >>> lsorted = qsort(l)
    >>> print(lsorted)
    [1, 3, 4, 5, 6, 7, 8, 9, 10]
    """
    if len(l) <= 1:
        return l
    return qsort([lt for lt in l[1:] if lt < l[0]]) + l[0:1] + \
        qsort([ge for ge in l[1:] if ge >= l[0]])


def kmp(text, pattern):
    """The famous Knuth-Morris-Pratt algorithm.

    Example:
    >>> g = kmp('dsafdsagdsafdsafsaga', 'dsa')
    >>> for e in g:
    ...     print(e)
    ...
    0
    4
    8
    12
    """
    pattern = list(pattern)
    length = len(pattern)
    shifts = [1] * (length + 1)
    shift = 1
    for pos, pat in enumerate(pattern):
        while shift <= pos and pat != pattern[pos-shift]:
            shift += shifts[pos-shift]
        shifts[pos+1] = shift

    start_pos = 0
    match_len = 0
    for c in text:
        while match_len == length or match_len >= 0 and pattern[match_len] != c:
            start_pos += shifts[match_len]
            match_len -= shifts[match_len]
        match_len += 1
        if match_len == length:
            yield start_pos


def find_iter(text, pattern):
    """A faster way than kmp().

    Example:
    >>> g = find_iter('dsafdsagdsafdsafsaga', 'dsa')
    >>> for e in g:
    ...     print(e)
    ...
    0
    4
    8
    12
    """
    pos = -1
    while True:
        pos = text.find(pattern, pos+1)
        if pos < 0:
            break
        yield pos


class Ratings(UserDict.DictMixin, dict):
    """A dict-like tool whose keys are sorted by values.

    Example:
    >>> r = Ratings({'bob': 30, 'john': 20})
    >>> r.update({'paul': 20, 'tom':10})
    >>> r.has_key('paul')
    True
    >>> [r.rating(k) for k in ['bob', 'paul', 'john', 'tom']]
    [3, 2, 1, 0]
    >>> r.keys()
    ['tom', 'john', 'paul', 'bob']
    >>> r.values()
    [10, 20, 20, 30]
    """

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self._rating = [(v, k) for k, v in dict.iteritems(self)]
        self._rating.sort()

    def copy(self):
        return Ratings(self)

    def __setitem__(self, k, v):
        # delegate most works to dict, handling self._rating
        if k in self:
            del self._rating[self.rating(k)]
        dict.__setitem__(self, k, v)
        insort_left(self._rating, (v, k))

    def __delitem__(self, k):
        del self._rating[self.rating(k)]
        dict.__delitem__(self, k)

    # Use the method from dict instead of DictMixin as possible.
    # it is faster.
    __len__ = dict.__len__
    __contains__ = dict.__contains__
    has_key = __contains__

    def __iter__(self):
        for v, k in self._rating:
            yield k

    iterkeys = __iter__

    def keys(self):
        return list(self)

    def rating(self, key):
        item = self[key], key
        i = bisect_left(self._rating, item)
        if item == self._rating[i]:
            return i
        raise LookupError("item not found in rating.")

    def get_val_by_rating(self, rating):
        return self._rating[rating][0]

    def get_key_by_rating(self, rating):
        return self._rating[rating][1]
