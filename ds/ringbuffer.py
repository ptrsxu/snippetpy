#!/usr/bin/env python
# -*- coding: utf-8 -*-

class RingBuffer(object):
    """ a ringbuffer not filled """
    def __init__(self, size_max):
        self.max = size_max
        self.data = []
    class __Full(object):
        """ a ringbuffer filled """
        def append(self, x):
            self.data[self.cur] = x
            self.cur = (self.cur + 1) % self.max
        def tolist(self):
            """ return the list with real order """
            return self.data[self.cur:] + self.data[:self.cur]
    def append(self, x):
        """ add an element at the end of the buffer """
        self.data.append(x)
        if len(self.data) == self.max:
            self.cur = 0
            # chang the state of the instance to "FULL" forever
            self.__class__ = self.__Full
    def tolist(self):
        """ return the list with real order """
        return self.data

def main():
    x = RingBuffer(5)
    x.append(1)
    x.append(2)
    x.append(3)
    x.append(4)
    print x.__class__, x.tolist()
    x.append(5)
    x.append(6)
    x.append(7)
    print x.__class__, x.tolist()
    x.append(8)
    x.append(9)
    x.append(10)
    print x.__class__, x.tolist()

if __name__=="__main__":
    main()
