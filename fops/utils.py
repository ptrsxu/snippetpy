#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
from python cookbook 2nd edition
A collection of functions helpful for file related opeartions.
"""

import os
import sys
import tempfile
import fnmatch
import glob
import itertools

def adapt_file(fobj):
    """adapt a file-like object into a real file object.

    example:
    >>> from cStringIO import StringIO
    >>> buf = StringIO('HelloWorld')
    >>> f = adapt_file(buf)
    >>> f.read()
    'HelloWorld'
    """
    CHUNK_SIZE = 16 * 1024
    if isinstance(fobj, file):
        return fobj

    tmp = tempfile.TemporaryFile()
    while True:
        data = fobj.read(CHUNK_SIZE)
        if not data:
            break
        tmp.write(data)
    fobj.close()
    tmp.seek(0)
    return tmp


def all_files(root, patterns='*', single_level=False, yield_folders=False):
    """Yield files/folders that match patterns.

    example:
    >>> for i in all_files('/', '*bin;ho*', True, True):
    ...     print(i)
    /bin
    /home
    /sbin
    """
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)
        files.sort()
        for f in files:
            for pattern in patterns:
                if fnmatch.fnmatch(f, pattern):
                    yield os.path.join(path, f)
                    break
        if single_level:
            break


def swap_ext(dirname, before, after):
    """change files with ext ``before`` to ``after`` in ``dirname``."""
    if before[0] != '.':
        before = '.' + before
    if after[0] != '.':
        after = '.' + after
    for path, subdirs, files in os.walk(dirname):
        for i in files:
            if i.endswith(before):
                old_name = os.path.join(path, i)
                new_name = os.path.join(path, i[:-len(before)]+after)
                os.rename(old_name, new_name)


def search_file(filename, search_paths, sep=os.pathsep):
    """search filename in the dirs showed by search_paths.

    example:
    >>> import os
    >>> search_file('ifconfig', os.getenv('PATH'))
    '/sbin/ifconfig'
    """
    for path in search_paths.split(sep):
        candidate = os.path.join(path, filename)
        if os.path.isfile(candidate):
            return os.path.abspath(candidate)
    return None


def all_match(search_paths, pattern, sep=os.pathsep):
    """yield files match pattern in all path of search_paths.

    example:
    >>> import os
    >>> for i in all_match(os.getenv('PATH'), 'ifco?fig'):
    ...     print(i)
    ...
    /sbin/ifconfig
    """
    for path in search_paths.split(sep):
        for match in glob.glob(os.path.join(path, pattern)):
            yield match


def _find_in_sys_path(pathname, match_func=os.path.isfile):
    for d in sys.path:
        for path, subdirs, files in os.walk(d):
            candidate = os.path.join(path, pathname)
            if match_func(candidate):
                return candidate
    return None


def file_in_sys_path(pathname):
    """Check if pathname is in sys.path or it's subdirs.

    example:
    >>> os.path.isfile(file_in_sys_path('os.py'))
    True
    """
    return _find_in_sys_path(pathname)


def dir_in_sys_path(path):
    """Check if path is in sys.path or it's subdirs.

    example:
    >>> os.path.isdir(dir_in_sys_path('distutils'))
    True
    """
    return _find_in_sys_path(path, match_func=os.path.isdir)


def all_equal(elements):
    return len(set(elements)) == 1


def common_prefix(*seq):
    """Returns the same prefix and the rest of a few sequences.

    example:
    >>> common_prefix('abcdefg', 'abcddgg', 'abcgggg')
    (['a', 'b', 'c'], ['defg', 'ddgg', 'gggg'])
    """
    if not seq:
        return [], []
    prefix = []
    left = []
    for elem in itertools.izip(*seq):
        if all_equal(elem):
            prefix.append(elem[0])
        else:
            break
    return prefix, [elem[len(prefix):] for elem in seq]


def related_path(p1, p2, sep=os.path.sep, pardir=os.path.pardir):
    """Returns the related path of p1 to p2.

    example:
    >>> related_path('/a/b/c/d', '/a/b/z/y/x')
    '../../z/y/x/'
    >>> related_path('/a', '/a/b/z/y/x')
    'b/z/y/x/'
    """
    if p1[-1] != sep:
        p1 = p1 + sep
    if p2[-1] != sep:
        p2 = p2 + sep
    prefix, (rest1, rest2) = common_prefix(p1, p2)
    if not prefix:
        return p2
    if not rest1:
        return rest2
    return sep.join([pardir]*len(rest1.strip(sep).split(sep)) + [rest2])
