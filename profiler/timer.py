#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time


class Timer:
    """
    A Timer which measures the elapsed time of an operation.
    Example:
    >>> t = Timer()
    >>> import time
    >>> def test():
    ...     time.sleep(2)
    >>> with t:
    ...     test()
    >>> 2.0 < t.elapsed < 2.1
    True
    """
    def __init__(self, func=time.perf_counter):
        self.elapsed = 0.0
        self._func = func
        self._start = None

    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = self._func()

    def stop(self):
        if self._start is None:
            raise RuntimeError('Not started')
        end = self._func()
        self.elapsed += end - self._start
        self._start = None

    def reset(self):
        self.elapsed = 0.0

    @property
    def running(self):
        return self._start is not None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()
