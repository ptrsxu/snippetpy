"""from python cookbook 2nd edition."""
from __future__ import print_function

import os
import sys
import re
import time
import datetime

def get_ptyreq_reply(line):
    # for Microsoft Windows, the `pty-req reply` in sshd log would be 0.
    # for Linux, the `pty-req reply` would be 1.
    REGEX = r'(?<=pty-req reply )\d'
    try:
        return re.search(REGEX, line).group(0)
    except AttributeError:
        return None


def get_pid(line):
    REGEX = r'(?<=sshd\[)\d+'
    try:
        return re.search(REGEX, line).group(0)
    except AttributeError:
        return None


def kill_conns_from_microsoft():
    AUTH_LOG_FILE = '/var/log/auth.log'
    # AUTH_LOG_FILE = '/var/log/secure'
    SSHD_CONFIG_FULE = '/etc/ssh/sshd_config'
    CMD = "/bin/sed -i.bak 's/LogLevel.*/LogLevel DEBUG1/g' %s" % SSHD_CONFIG_FULE

    sys.stderr.write('configuring the LogLevel to DEBUG1...\n')
    try:
        os.system(CMD)
    except:
        sys.stderr.write('You may need to configure LogLevel to DEBUG1\
                manually in file /etc/ssh/sshd_config. and restart this\
                program later.\n')

    sys.stderr.write("sshd breaking windows connections\
            daemon started with pid %d\n" % os.getpid())

    while True:
        for line in open(AUTH_LOG_FILE):
            if get_ptyreq_reply(line) == '0':
                try:
                    os.kill(int(get_pid(line)), 9)
                    print('[%s, KILLED:] %s' %
                            (datetime.datetime.now(), line),
                            file=sys.stderr)
                except OSError:
                    continue
        time.sleep(1)


