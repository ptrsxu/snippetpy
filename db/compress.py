#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gzip

try:
    import cPickle as pickle
except ImportError:
    import pickle

def save_pgz(filename, *objs):
    """save objects into compressed file."""
    f = gzip.open(filename, 'wb')
    for o in objs:
        pickle.dump(o, f, proto=2)
    f.close()

def load_pgz(filename):
    """load objects from compressed file."""
    f = gzip.open(filename, 'rb')
    while True:
        try:
            yield pickle.load(f)
        except EOFError:
            break
    f.close()

