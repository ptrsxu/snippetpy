#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Some useful funcitons or classes for text handling.
"""
from __future__ import absolute_import
import string
from snippetpy import PY3


def reverse(s):
    """reverse a string by character, including unicode. Another method can
    be: ``''.join(reversed(s))`` .
    """
    return s[::-1]


def _translator(frm='', to='', delete='', keep=None):
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


def _makefilter(keep):
    """generate a filter which accepts a string and returns another that
    contains characters only from the ``keep`` .

    This is only for python 2 becuase the ``maketrans`` funciton returns
    a dict in python 3.
    Example:

    >>> f = makefilter('12345!@#$%abcde')
    >>> f('Hello World! Welcome to China, ~!@#$%^&*().')
    'ed!ecea!@#$%'
    """
    all_chars = string.maketrans('', '')
    del_chars = all_chars.translate(all_chars, keep)
    def thefilter(s):
        return s.translate(all_chars, del_chars)
    return thefilter


class _Keeper(object):
    """Same like ``_makefilter`` and can be used for unicode strings.
    example:

    >>> aeiou = Keeper('aeiou')
    >>> aeiou('i am peter, who are you?')
    u'iaeeoaeou'
    """

    def __init__(self, keep):
        self.keep = set(map(ord, keep))

    def __getitem__(self, n):
        if n not in self.keep:
            return None
        return unichr(n)

    def __call__(self, s):
        return unicode(s).translate(self)

def expand_by_marker(fmt, d, marker='"', safe=False):
    """expand a string which may have some items quoted by ``marker`` , expand
    them with the content in ``d`` . use ``""`` in the ``fmt`` to represent a
    literal ``"`` . We can use the ``string.Template`` class to do this(both
    in python2 or python3) also. However, only the prefix marker is necessary
    in ``string.Template`` .
    example:

    >>> expand_by_marker('My name is "name", my age is "age".',
    ...                  {'name': 'peter', 'age': '5'})
    'My name is peter, my age is 5.'
    """

    if safe:
        def lookup(k):  return d.get(k, k.join(marker*2))
    else:
        def lookup(k):  return d[k]

    parts = fmt.split(marker)
    parts[1::2] = map(lookup, parts[1::2])
    return ''.join(parts)


import re
def multiple_replace(text, adict):
    """
    example:
    >>> multiple_replace('my name is $name, my age is $age',
    ...                  {'$name':'peter', '$age':'5'})
    'my name is peter, my age is 5'
    """
    regex = re.compile('|'.join(map(re.escape, adict)))
    def one_xlat(match):
        return adict[match.group(0)]
    return regex.sub(one_xlat, text)

class MultiReplacer():
    """replace some words in a string. If the words match the keys of a given
    dict, we substitute the keys with related values.
    example:

    >>> sa = 'he is a good man, i am a good man, we are good people!'
    >>> d = {'is':'wanna be', 'am':'wanna be', 'are':'wanna be'}
    >>> replacer = MultiReplacer(d)
    >>> replacer(sa)
    'he wanna be a good man, i wanna be a good man, we wanna be good people!'
    """
    def __init__(self, *args, **kwards):
        self.adict = dict(*args, **kwards)
        self.reobj = self.make_reobj()
    # change the re object policy by overriding the below method
    def make_reobj(self):
        return re.compile('|'.join(map(re.escape, self.adict)))
    def get_match(self, match):
        return self.adict[match.group(0)]
    def __call__(self, s):
        return self.reobj.sub(self.get_match, s)


class istr(str):
    """A string acts like ``str`` except that the operation of compare
    and query is case insensitive.
    """
    def __init__(self, *args):
        self._lowered = str.lower(self)
    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, str.__repr__(self))
    def __hash__(self):
        return hash(self._lowered)
    def lower(self):
        return self._lowered

def _make_case_insensitive(name):
    str_meth = getattr(str, name)
    def x(self, other, *args):
        try: other = other.lower()
        except (TypeError, AttributeError, ValueError): pass
        return str_meth(self._lowered, other, *args)
    setattr(istr, name, x)

for name in 'eq lt le gt ge ne contains'.split():
    _make_case_insensitive('__%s__' % name)
for name in 'count endswith find index rfind rindex startswith'.split():
    # replace, split strip can also be added.
    _make_case_insensitive(name)


if PY3:
    translator = None
    makefilter = None
    Keeper = None
else:
    translator = _translator
    makefilter = _makefilter
    class Keeper(_Keeper): pass
