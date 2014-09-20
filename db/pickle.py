#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""from python cookbook 2nd edition."""


class PrettyClever(object):
    """A sample of user defined class that can be dump/load by pickle."""
    def __init__(self, *args):
        self.args = args

    def __getstate__(self):
        def normalize(x):
            # special operations on file objects.
            if isinstance(x, file):
                return 1, (x.name, x.mode, x.tell())
            return 0, x
        return [normalize(x) for x in self.args]

    def __setstate__(self, state):
        def reconstruct(x):
            if x[0] == 0:
                return x[1]
            name, mode, offset = x[1]
            f = open(name, mode)
            f.seek(offset)
            return f
        self.args = tuple([reconstruct(x) for x in state])
