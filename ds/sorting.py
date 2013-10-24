#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A collection of tools for sorting and searching.
"""

import operator
import re
import heapq

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
