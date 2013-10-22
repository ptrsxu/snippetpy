#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import print_function

from snippetpy import PY3

if PY3:
    from io import StringIO
else:
    from cStringIO import StringIO

class RewindableFile(object):
    """Encapsulates a file-like object to be rewindable."""
    def __init__(self, input_file):
        self.f = input_file
        self.buffer_file = StringIO()
        self.at_start = True
        try:
            self.start = input_file.tell()
        except (IOError, AttributeError):
            self.start = 0
        self._use_buffer = True

    def seek(self, offset, whence=0):
        if whence != 0:
            raise ValueError("whence=%r; expecting 0." % whence)
        if offset != self.start:
            raise ValueError("offset=%r; expecting %s." % (offset, self.start))
        self.rewind()

    def rewind(self):
        """Back to the begining of the file[-like] object."""
        self.buffer_file.seek(0)
        self.at_start = True

    def tell(self):
        """Return the current position of the file."""
        if not self.at_start:
            raise TypeError("RewindableFile cannot tell except at start\
                    of the file.")
        return self.start

    def _read(self, size):
        if size < 0:
            total = self.f.read()
            if self._use_buffer:
                self.buffer_file.write(total)
            return self.buffer_file.read() + total
        elif size == 0:
            return ""

        chunk = self.buffer_file.read(size)
        if len(chunk) < size:
            left = self.f.read(size - len(chunk))
            if self._use_buffer:
                self.buffer_file.write(left)
            return chunk + left
        return chunk

    def read(self, size=-1):
        """read ``size`` bytes, read to the end if size equals -1."""
        chunk = self._read(size)
        if self.at_start and chunk:
            self.at_start = False
        self._check_no_buffer()
        return chunk

    def readline(self):
        s = self.buffer_file.readline()
        if s[-1:] == '\n':
            return s
        t = self.f.readline()
        if self._use_buffer:
            self.buffer_file.write(t)
        self._check_no_buffer()
        return s + t

    def readlines(self):
        return self.read().splitlines(True)

    def _check_no_buffer(self):
        if not self._use_buffer and \
                self.buffer_file.tell() == len(self.buffer_file.getvalue()):
            for n in 'seek tell read readline readlines'.split():
                setattr(self, n, getattr(self.f, n, None))
            del self.buffer_file

    def no_buffer(self):
        """Stop using buffer if it runs out."""
        self._use_buffer = False
