#!/usr/bin/env python
"""from python cookbook 2nd edition."""
import UserDict

class ChainMap(object):
    """A collection of mappings whose items are easy to check and fetch.

    Example:
    >>> cm = ChainMap({'name': 'Peter', 'age': 5}, {'lang': 'py'})
    >>> cm.get('name')
    'Peter'
    >>> cm.get('salary') == None
    True
    >>> 'lang' in cm
    True
    """
    def __init__(self, *mappings):
        self._mappings = mappings
    def __getitem__(self, k):
        for m in self._mappings:
            try:
                return m[k]
            except KeyError:
                pass
        raise KeyError(k)
    def get(self, k, default=None):
        try:
            return self[k]
        except KeyError:
            return default
    def __contains__(self, k):
        try:
            self[k]
            return True
        except KeyError:
            return False


class FullChainMap(ChainMap, UserDict.DictMixin):
    def copy(self):
        return self.__class__(self._mappings)
    def __iter__(self):
        seen = set()
        for m in self._mappings:
            for k in m:
                if not k in seen:
                    yield k
                    seen.add(k)

    iterkeys = __iter__

    def keys(self):
        return list(self)

