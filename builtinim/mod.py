#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
from python cookbook 2nd edition.
"""

def import_by_name(modulename, name):
    """import a named object from a module."""
    try:
        module = __import__(modulename, globals(), locals(), [name])
    except ImportError:
        return None
    return getattr(modulename, name)
