#!/usr/bin/env python

class Readonly(object):

    class ROError(AttributeError):
        pass

    mutators = {
            list: set('''__delitem__ __delslice__ __iadd__ __imul__
                    __setitem__ __setslice__ append extend insert
                    pop remove sort'''.split()),
            dict: set('''__delitem__ __setitem__ clear pop popitem
                    setdefault update'''.split())
            }

    def __init__(self, o):
        object.__setattr__(self, '_o', o)
        object.__setattr__(self, '_no', self.mutators.get(type(o), ()))

    def __setattr__(self, name, value):
        raise Readonly.ROError('Cannot set attr on RO objects.')

    def __delattr__(self, name):
        raise Readonly.ROError('Cannot del attr on RO objects.')

    def __getattr__(self, name):
        if name in self._no:
            raise Readonly.ROError('Cannot set attr on RO objects.')
        return getattr(self._o, name)

    def __iter__(self):
        for e in self._o:
            yield e
