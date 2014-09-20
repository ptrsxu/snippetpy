#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
from python cookbook 3rd edition
daemonize the current process

no need to daemonize the process if it's started by 'initd'(which means you
may only need to 'chdir()' or 'umask()')

this function runs for PY2.6=+ & PY3
"""

import os
import sys
import atexit
import signal


def daemonize(pidfile,
              stdin="/dev/null",
              stdout="/dev/null",
              stderr="/dev/null"):

    if os.path.exists(pidfile):
        sys.stderr.write("already running")
        sys.exit(1)

    # the first fork(), shell returns after this.
    try:
        pid = os.fork()
        if pid > 0:
            # the first parent process exits.
            sys.exit(0)
    except OSError as e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    # seperate from the parent env
    os.chdir("/")
    os.umask(0)

    # amke the child session leader. (if it opens any terminal,
    # the terminal will be the control terminal, we don't need
    # a control terminal so that we fork() the second time.)
    os.setsid()

    # the second fork()
    try:
        pid = os.fork()
        if pid > 0:
            # the second parent process exits.
            sys.exit(0)
    except OSError as e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    # afther the second fork, the child will never be a session leader.
    # now it's daemon process, redirect the fds
    sys.stdout.flush()
    sys.stderr.flush()

    with open(stdin, 'rb', 0) as f:
        os.dup2(f.fileno(), sys.stdin.fileno())

    with open(stdout, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stdout.fileno())

    with open(stderr, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stderr.fileno())

    # write the pidfile
    with open(pidfile, 'w') as f:
        f.write("%s\n" % str(os.getpid()))

    # remove the pidfile
    atexit.register(lambda: os.remove(pidfile))

    def sigterm_handler(signo, frame):
        sys.stderr.write("terminated by signal!\n")
        sys.exit(1)

    signal.signal(signal.SIGTERM, sigterm_handler)


def main():
    import time
    sys.stdout.write("daemon started with pid %d\n" % os.getpid())
    sys.stdout.write("daemon stdout output\n")
    sys.stderr.write("daemon stderr output\n")
    c = 0
    while True:
        sys.stdout.write("%d: %s\n" % (c, time.ctime()))
        sys.stdout.flush()
        c = c + 1
        time.sleep(1)


if __name__ == "__main__":
    daemonize("/tmp/daemon.pid",
              "/dev/null",
              "/tmp/daemon.log",
              "/tmp/daemon.log")
    main()
