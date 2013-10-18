#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, ftplib

def is_ftp_site_up(site):
    try:
        ftplib.FTP(site).quit()
    except socket.error:
        return False
    else:
        return True

def ftp_sites_filter(sites):
    return [site for site in sites if is_ftp_site_up(site)]
