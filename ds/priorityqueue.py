#!/usr/bin/env python

"""from python cookbook 2nd edition."""
import Queue
import heapq
import time


class PriorityQueue(Queue.Queue):
    # initial
    def _init(self, maxsize):
        self.maxsize = maxsize
        self.queue = []

    # return length of subitems in queue
    def _qsize(self):
        return len(self.queue)

    # check if the queue is empty
    def _empty(self):
        return not self.queue

    # check if the queue is full
    def _full(self):
        return self.maxsize > 0 and len(self.queue) >= self.maxsize

    # append a new element to queue
    def _put(self, item):
        heapq.heappush(self.queue, item)

    # get an element from queue
    def _get(self):
        return heapq.heappop(self.queue)

    # real put and get
    def put(self, item, priority=0, block=True, timeout=None):
        decorated_item = priority, time.time(), item
        Queue.Queue.put(self, decorated_item, block, timeout)

    def get(self, block=True, timeout=None):
        priority, time_posted, item = Queue.Queue.get(self, block, timeout)
        return item
