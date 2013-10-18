#!/usr/bin/env python

"""
Author: xupeng@redflag-linux.com
License: GPL

ioctl defines for python, generally from asm-generic/ioctl.h of kernel source code.

"""

_IOC_NRBITS = 8
_IOC_TYPEBITS = 8

# Let any architecture override either of the following before
# including this file.
_IOC_SIZEBITS = 14
_IOC_DIRBITS = 2

_IOC_NRMASK = (1 << _IOC_NRBITS) - 1
_IOC_TYPEMASK = (1 << _IOC_TYPEBITS) - 1
_IOC_SIZEMASK = (1 << _IOC_SIZEBITS) - 1
_IOC_DIRMASK = (1 << _IOC_DIRBITS) - 1

_IOC_NRSHIFT = 0
_IOC_TYPESHIFT = _IOC_NRSHIFT + _IOC_NRBITS
_IOC_SIZESHIFT = _IOC_TYPESHIFT + _IOC_TYPEBITS
_IOC_DIRSHIFT = _IOC_SIZESHIFT + _IOC_SIZEBITS


# Direction bits, which any architecture can choose to override
# before including this file.
_IOC_NONE = 0x0
_IOC_WRITE = 0x1
_IOC_READ = 0x2


def _IOC(_dir, _type, _nr, _size):
    return (_dir << _IOC_DIRSHIFT) | (_type << _IOC_TYPESHIFT) | (_nr << _IOC_NRSHIFT) | (_size << _IOC_SIZESHIFT)


# used to create numbers ...
def _IO( _type, _nr):
    return _IOC(_IOC_NONE, _type, _nr, 0)

def _IOR( _type, _nr, _size):
    return _IOC(_IOC_READ, _type, _nr, _size)

def _IOW(_type, _nr, _size):
    return _IOC(_IOC_WRITE, _type, _nr, _size)

def _IOWR(_type, _nr, _size):
    return _IOC(_IOC_READ|_IOC_WRITE, _type, _nr, _size)

def _IOR_BAD(_type, _nr, _size):
    return _IOC(_IOC_READ, _type, _nr, _size)

def _IOW_BAD(_type, _nr, _size):
    return _IOC(_IOC_WRITE, _type, _nr, _size)

def _IOWR_BAD(_type, _nr, _size):
    return _IOC(_IOC_READ|_IOC_WRITE, _type, _nr, _size)


# used to decode ioctl numbers..
def _DIR(_nr):
    return (_nr >> _IOC_DIRSHIFT) & _IOC_DIRMASK

def _TYPE(_nr):
    return (_nr >> _IOC_TYPESHIFT) & _IOC_TYPEMASK

def _NR(_nr):
    return (_nr >> _IOC_NRSHIFT) & _IOC_NRMASK

def _SIZE(_nr):
    return (_nr >> _IOC_SIZESHIFT) & _IOC_SIZEMASK


# ... and for the drivers/sound files...
IOC_IN = _IOC_WRITE << _IOC_DIRSHIFT
IOC_OUT = _IOC_READ << _IOC_DIRSHIFT
IOC_INOUT = (_IOC_WRITE | _IOC_READ) << _IOC_DIRSHIFT
IOCSIZE_MASK = _IOC_SIZEMASK << _IOC_SIZESHIFT
IOCSIZE_SHIFT = _IOC_SIZESHIFT



