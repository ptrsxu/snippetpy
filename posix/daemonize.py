#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
daemonize the current process

no need to daemonize the process if it's started by 'initd'(which means you
may only need to 'chdir()' or 'umask()')
"""

import os, sys

def daemonize(stdin = "/dev/null",
        stdout = "/dev/null",
        stderr = "/dev/null"):
    # the first fork(), shell returns after this.
    try:
        pid = os.fork()
        if pid > 0:
            # the first parent process exits.
            sys.exit(0)
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    # seperate from the parent env
    os.chdir("/")
    os.umask(0)

    # amke the child session leader. (if it opens any terminal, the terminal will
    # be the control terminal, we don't need a control terminal so that we fork()
    # the second time.)
    os.setsid()

    # the second fork()
    try:
        pid = os.fork()
        if pid > 0:
            # the second parent process exits.
            sys.exit(0)
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    # afther the second fork, the child will never be a session leader.
    # now it's daemon process, redirect the fds
    for f in sys.stdout, sys.stderr: f.flush()
    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


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

if __name__=="__main__":
    daemonize("/dev/null", "/tmp/daemon.log", "/tmp/daemon.log")
    main()



