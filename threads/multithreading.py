#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
run a function simultaneously with different args
"""
import threading, time, Queue

class MultiThread(object):
    def __init__(self,
            function,
            args_vector,
            max_threads = 5,
            queue_results = False):
        self._function = function
        self._lock = threading.Lock()
        self._next_args = iter(args_vector).next
        self._thread_pool = [ threading.Thread(target = self._dosome)
                for i in range(max_threads) ]
        if queue_results:
            self._queue = Queue.Queue()
        else:
            self._queue = None
    def _dosome(self):
        while True:
            self._lock.acquire()
            try:
                try:
                    args = self._next_args()
                except StopIteration:
                    break
            finally:
                self._lock.release()
            result = self._function(args)
            if self._queue is not None:
                self._queue.put((args, result))
    def get(self, *a, **kw):
        if self._queue is not None:
            return self._queue.get(*a, **kw)
        else:
            raise ValueError, 'Not queueing results'
    def start(self):
        for thread in self._thread_pool:
            time.sleep(0)
            thread.start()
    def join(self, timeout = None):
        for thread in self._thread_pool:
            thread.join(timeout)

def main():
    import random
    def recite_n_times_table(n):
        for i in range(2, 11):
            print "%d * %d = %d" % (n, i, n*i)
            time.sleep(0.3 + 0.3 * random.random())
    mt = MultiThread(recite_n_times_table, range(2, 11))
    mt.start()
    mt.join()
    print "Well done!"

if __name__=="__main__":
    main()


