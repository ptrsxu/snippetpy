#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""from python cookbook 2rd edition"""

import sys

class Progressbar(object):
    def __init__(self, finalcount, block_char = "."):
        self.finalcount = finalcount
        self.blockcount = 0
        self.block = block_char
        self.f = sys.stdout
        if not self.finalcount: return
        self.f.write("\n--------------------- % Progress ----------------1\n")
        self.f.write("    1    2    3    4    5    6    7    8    9    0\n")
        self.f.write("----0----0----0----0----0----0----0----0----0----0\n")
    def progress(self, count):
        count = min(count, self.finalcount)
        if self.finalcount:
            percentcomplete = int(round(100.0 * count / self.finalcount))
            if percentcomplete < 1: percentcomplete = 1
        else:
            percentcomplete = 100
        blockcount = int(percentcomplete // 2)
        if blockcount <= self.blockcount:
            return
        for i in range(self.blockcount, blockcount):
            self.f.write(self.block)
        self.f.flush()
        self.blockcount = blockcount
        if percentcomplete == 100:
            self.f.write("\n")


def main():
    from time import sleep
    print "test:"
    pb = Progressbar(8, "*")
    for count in range(1, 9):
        pb.progress(count)
        sleep(0.2)

    print "test 100:"
    pb = Progressbar(100)
    pb.progress(20)
    sleep(0.3)
    pb.progress(40)
    sleep(0.3)
    pb.progress(55)
    sleep(0.3)
    pb.progress(90)
    sleep(0.3)
    pb.progress(100)
    sleep(0.3)

    print "test 1:"
    pb = Progressbar(1)
    pb.progress(1)

if __name__=="__main__":
    main()
