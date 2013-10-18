#!/usr/bin/env python
# -*- coding: utf-8 -*-

class fifo(list):
    """a FIFO, use append() for input and pop() for output."""
    def __init__(self):
        self.back = []
        self.append = self.back.append
    # a O(1) pop()
    def pop(self):
        if not self:
            self.back.reverse()
            self[:] = self.back
            del self.back[:]
        return super(fifo, self).pop()

class fifolist(list):
    """a FIFO, use append() for input and pop() for output."""
    # a O(n) pop()
    def pop(self):
        return super(fifolist, self).pop(0)
