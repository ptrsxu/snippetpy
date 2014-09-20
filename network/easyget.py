#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""from python cookbook 2nd edition."""

import sys, urllib

def reporthook(*a):
    """ (block_num, block_size, total_size) """
    print a

for url in sys.argv[1:]:
    i = url.rfind('/')
    filename = url[i+1:]
    print url, "--->", filename
    urllib.urlretrieve(url, filename, reporthook)

