#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
from python cookbook 2nd edition.
some tools for integers, strings, list, tuple, dict etc. Most of which are
BUILTIN modules IMproved.
"""

import string
import random
import heapq


def reverse(s):
    """reverse a string by character, including unicode. Another method can
    be: ``''.join(reversed(s))`` .
    """
    return s[::-1]


def translator(frm='', to='', delete='', keep=None):
    """generate a translator which can be called on a string for substituting
    ``frm`` to ``to`` , deleting ``delete`` and keep the ``keep`` . This
    funciton is only for python 2 becuase the ``maketrans`` funciton returns
    a dict in python 3.

    examples:

    >>> trans = translator('1234567890', '!@#$%^&*()')
    >>> trans('a1b2c3d4e5f6g7')
    'a!b@c#d$e%f^g&'
    >>> trans = translator('1234567890', '!@#$%^&*()', '123')
    >>> trans('a1b2c3d4e5f6g7')
    'abcd$e%f^g&'
    >>> trans = translator('1234567890', '!@#$%^&*()', '123', '345')
    >>> trans('a1b2c3d4e5f6g7')
    '$%'
    >>> trans = translator('1234567890', '!@#$%^&*()', '123', '345ab')
    >>> trans('a1b2c3d4e5f6g7')
    'ab$%'
    """
    if len(to) == 1:
        to = to * len(frm)

    table = string.maketrans(frm, to)
    if keep is not None:
        all_chars = string.maketrans('', '')
        delete = all_chars.translate(all_chars,
                                     keep.translate(all_chars, delete))

    def translate(s):
        return s.translate(table, delete)

    return translate


def list_get(l, i, v=None):
    """This function gets an item from a list if it exists. It's faster than
    most of the other methods.
    """
    if -len(l) <= i < len(l):
        return l[i]
    else:
        return v


def list_or_tuple(arg):
    """determine if arg is a list or tuple """
    return isinstance(arg, (list, tuple))


def flatten(seq, to_expand=list_or_tuple):
    """to flatten the list or tuple (even if any member includes embeded list
    or tuple).
    """
    for item in seq:
        if to_expand(item):
            for subitem in flatten(item, to_expand):
                yield subitem
        else:
            yield item


def dict_from_list(l):
    """generate a dict use l[0], l[2], l[4]... as key, and l[1], l[3], l[5]...
    as value. the last key would be ignored if len(l) is odd.
    """
    return dict(zip(l[::2], l[1::2]))


def sub_dict(d, subkeys, default=None):
    """ return a new dict with subkeys and related values  """
    return dict([(k, d.get(k, default)) for k in subkeys])


def invert_dict(d):
    """generate a dict with (v, k), (v, k) are values and keys from d."""
    return dict([(v, k) for k, v in d.items()])


def invert_dict_fast(d):
    """fast version of invert_dict"""
    return dict(zip(d.values(), d.keys()))


def random_pick(elem_list, chance_list):
    """get an emlement from elem_list, the probability of each member is stored
    in chance_list. each member of chance_list is between 0.0 and 1.0, and
    the sum of chance_list should be 1.0
    """
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(elem_list, chance_list):
        cumulative_probability += item_probability
        if x < cumulative_probability:
            break
    return item


def random_picks(elem_list, chance_list):
    """same as random_pck(), but the member of chance_list is integer and
    it's >= 0.
    """
    table = [z for x, y in zip(elem_list, chance_list) for z in [x] * y]
    while True:
        yield random.choice(table)


def is_a_number(s):
    """test if s is a number(integer or float)"""
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True


def unique(s):
    """returns an unordered list, without any repeat!"""
    try:
        # method 1: O(n)
        return list(set(s))
    except TypeError:
        pass

    # method 2: O(nlog(n))
    # if set() doesn't work
    t = list(s)
    try:
        t.sort()
        # if i == 0, of course we need it, and we must avoid 0 - 1 !
        return [x for i, x in enumerate(t) if not i or x != t[i-1]]
    except TypeError:
        del t

    # method 3: O(n^2)
    u = []
    for x in s:
        if x not in u:
            u.append(x)
    return u


def sample(n, r):
    """
    random samples without replacement, refer to Donald E. Knuth TAOCP sec3.4.2
    generate r numbers from [0, n] with order, better mem use than
    random.sample
    """
    rand = random.random
    population = n
    for samp in xrange(r, 0, -1):
        cumprob = 1.0
        x = rand()
        while x < cumprob:
            cumprob -= cumprob * samp / population
            population -= 1
        yield n - population - 1


def sample_wr(population, _choose=random.choice):
    """random samples with replacement"""
    while True:
        yield _choose(population)


def memoize(fn):
    """Memoizing, only for pure functions(without dependence of outer vars,such
    as global vars). It stores the results of the functions in a dict with
    their arguments as keys
    Usage:  def func(p): pass
            func = memoize(func)
        or
            @memoize
            def func(p): pass
    """
    memo = {}

    def memoizer(*param_tuple, **kwds_dict):
        if kwds_dict:
            memoizer.namedargs += 1
            return fn(*param_tuple, **kwds_dict)
        try:
            # if the arguments are hashable and position based, we cache it!
            # mutable arguments(with result) will not be cached!
            # named arguments(with result) will not be cached!
            memoizer.cacheable += 1
            try:
                return memo[param_tuple]
            except KeyError:
                memoizer.misses += 1
                memo[param_tuple] = result = fn(*param_tuple)
                return result
        except TypeError:
            memoizer.cacheable -= 1
            memoizer.noncacheable += 1
            return fn(*param_tuple)
    memoizer.namedargs = memoizer.cacheable = memoizer.noncacheable = 0
    memoizer.misses = 0
    return memoizer


def empty_copy(obj):
    """Avoid the calling of __init__ of other instance.

    This is usually used in the __copy__ method of some class. After
    calling this, we can call newcopy.__dict__.update(self.__dict__)
    to get most of the attributes.
    """
    class _Empty(obj.__class__):
        def __init__(self):
            pass
    newcopy = _Empty()
    newcopy.__class__ = obj.__class__
    return newcopy


def large_merge(*seqs):
    """Merge some ordered sequences, some of them are pretty large.

    Example:
    >>> la = [1, 3, 5, 7]
    >>> lb = [2, 4]
    >>> lc = [14, 19]
    >>> lall = []
    >>> for i in large_merge(la, lb, lc):
    ...     lall.append(i)
    ...
    >>> lall
    [1, 2, 3, 4, 5, 7, 14, 19]
    """
    heap = []
    for seq in seqs:
        it = iter(seq)
        for current_val in it:
            heap.append((current_val, it))
            break
    heapq.heapify(heap)
    while heap:
        current_val, it = heap[0]
        yield current_val
        for current_val in it:
            heapq.heapreplace(heap, (current_val, it))
            break
        else:
            heapq.heappop(heap)


def main():
    l1 = [1, 2, 3, [4, 5, 6, (7, 8, 9), [10, 11], 12], 13]
    print(l1)
    for i in flatten(l1):
        print(i)

    l2 = [x for x in range(11, 22)]
    print(dict_from_list(l2))

    d1 = dict(k1=1, k2=2, k3=3, k4=4, k5=5, k6=6)
    subkeys = ['k1', 'k3', 'k5']
    print(sub_dict(d1, subkeys))

    d2 = invert_dict(d1)
    print('d2: ' + str(d2))

    d3 = invert_dict_fast(d1)
    print('d3: ' + str(d3))

    d4 = '3.14'
    print("d4.isdigit(): %s" % d4.isdigit())
    print("d4.is_a_number(): %s" % is_a_number(d4))

    print("--------------------------------------------------")

    def fib(n):
        if n < 2:
            return 1
        return fib(n-1) + fib(n-2)

    print("testing fib without memoizer")
    print("fib(38):")
    print(fib(38))
    print("testing fib withmemoizer, this would be much faster...")
    print("memoized fib(38):")
    fib = memoize(fib)
    print(fib(38))

if __name__ == '__main__':
    main()
