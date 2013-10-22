#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
A collection of functions helpful for file related opeartions.
"""

import os
import tempfile
import fnmatch
import glob

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
    >>> for i in all_match(os.getenv('PATH'), 'powe?off'):
    ...     print(i)
    ...
    /sbin/poweroff
    """
    for path in search_paths.split(sep):
        for match in glob.glob(os.path.join(path, pattern)):
            yield match

