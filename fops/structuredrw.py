#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
from `Python Cookbook` 3rd Edition:
    6.12. Reading Nested and Variable-Sized Binary Structures

This code only works for PY3
"""

###############################################################################
# the simple way(without meta class)
###############################################################################
import struct


class StructField(object):
    '''
    Descriptor representing a simple structure field
    '''
    def __init__(self, format, offset):
        self.format = format
        self.offset = offset

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            r = struct.unpack_from(self.format,
                                   instance._buffer,
                                   self.offset)
            return r[0] if len(r) == 1 else r


class Structure(object):
    def __init__(self, bytedata):
        self._buffer = memoryview(bytedata)


class PolyHeader(Structure):
    """
    example:
    >>> import struct
    >>> ba = bytearray(40)
    >>> struct.pack_into('<i', ba, 0, 1)
    >>> struct.pack_into('<d', ba, 4, 2.2)
    >>> struct.pack_into('<d', ba, 12, 3.3)
    >>> struct.pack_into('<d', ba, 20, 4.4)
    >>> struct.pack_into('<d', ba, 28, 5.5)
    >>> struct.pack_into('<i', ba, 36, 6)
    >>> len(ba)
    40
    >>> ba[0]
    1
    >>> ph = PolyHeader(ba)
    >>> ph.file_code
    1
    >>> ph.min_x
    2.2
    >>> ph.min_y
    3.3
    >>> ph.max_x
    4.4
    >>> ph.max_y
    5.5
    >>> ph.num_polys
    6
    """
    file_code = StructField('<i', 0)
    min_x = StructField('<d', 4)
    min_y = StructField('<d', 12)
    max_x = StructField('<d', 20)
    max_y = StructField('<d', 28)
    num_polys = StructField('<i', 36)


###############################################################################
# The better way dealing with non-nested structures(using meta class)
#   Using the former `StructField`
###############################################################################
class StructureMeta(type):
    '''
    Metaclass that automatically creates StructField descriptors
    '''
    def __init__(self, clsname, bases, clsdict):
        fields = getattr(self, '_fields_', [])
        byte_order = ''
        offset = 0
        for format, fieldname in fields:
            if format.startswith(('<','>','!','@')):
                byte_order = format[0]
                format = format[1:]
            format = byte_order + format
            setattr(self, fieldname, StructField(format, offset))
            offset += struct.calcsize(format)
        setattr(self, 'struct_size', offset)


class Structure2(metaclass=StructureMeta):
    def __init__(self, bytedata):
        self._buffer = bytedata

    @classmethod
    def from_file(cls, f):
        return cls(f.read(cls.struct_size))


class PolyHeader2(Structure2):
    """
    example:
    >>> import struct
    >>> ba = bytearray(40)
    >>> struct.pack_into('<i', ba, 0, 1)
    >>> struct.pack_into('<d', ba, 4, 2.2)
    >>> struct.pack_into('<d', ba, 12, 3.3)
    >>> struct.pack_into('<d', ba, 20, 4.4)
    >>> struct.pack_into('<d', ba, 28, 5.5)
    >>> struct.pack_into('<i', ba, 36, 6)
    >>> len(ba)
    40
    >>> ba[0]
    1
    >>> ph = PolyHeader2(ba)
    >>> ph.file_code
    1
    >>> ph.min_x
    2.2
    >>> ph.min_y
    3.3
    >>> ph.max_x
    4.4
    >>> ph.max_y
    5.5
    >>> ph.num_polys
    6
    """
    _fields_ = [
        ('<i', 'file_code'),
        ('d', 'min_x'),
        ('d', 'min_y'),
        ('d', 'max_x'),
        ('d', 'max_y'),
        ('i', 'num_polys')
    ]


###############################################################################
# The better way dealing with nested structures(using meta class)
#   Using a totally new structure field `NestedStructField`
###############################################################################
class NestedStructField(object):
    '''
    Descriptor representing a nested structure
    '''
    def __init__(self, name, struct_type, offset):
        self.name = name
        self.struct_type = struct_type
        self.offset = offset
    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            data = instance._buffer[self.offset:
                                    self.offset+self.struct_type.struct_size]
            result = self.struct_type(data)
            # Save resulting structure back on instance to avoid
            # further recomputation of this step
        setattr(instance, self.name, result)
        return result


class StructureMeta2(type):
    '''
    Metaclass that automatically creates StructField descriptors
    '''
    def __init__(self, clsname, bases, clsdict):
        fields = getattr(self, '_fields_', [])
        byte_order = ''
        offset = 0
        for format, fieldname in fields:
            if isinstance(format, StructureMeta2):
                setattr(self, fieldname,
                        NestedStructField(fieldname, format, offset))
                offset += format.struct_size
            else:
                if format.startswith(('<','>','!','@')):
                    byte_order = format[0]
                    format = format[1:]
                format = byte_order + format
                setattr(self, fieldname, StructField(format, offset))
                offset += struct.calcsize(format)

        setattr(self, 'struct_size', offset)


class Structure3(metaclass=StructureMeta2):
    def __init__(self, bytedata):
        self._buffer = bytedata

    @classmethod
    def from_file(cls, f):
        return cls(f.read(cls.struct_size))


class Point(Structure3):
    _fields_ = [
        ('<d', 'x'),
        ('d', 'y')
    ]

    def __str__(self):
        return '({}, {})'.format(
            getattr(self, 'x'),
            getattr(self, 'y')
        )


class PolyHeader3(Structure3):
    """
    example:
    >>> import struct
    >>> ba = bytearray(40)
    >>> struct.pack_into('<i', ba, 0, 1)
    >>> struct.pack_into('<d', ba, 4, 2.2)
    >>> struct.pack_into('<d', ba, 12, 3.3)
    >>> struct.pack_into('<d', ba, 20, 4.4)
    >>> struct.pack_into('<d', ba, 28, 5.5)
    >>> struct.pack_into('<i', ba, 36, 6)
    >>> len(ba)
    40
    >>> ba[0]
    1
    >>> ph = PolyHeader3(ba)
    >>> ph.file_code
    1
    >>> print(ph.min)
    (2.2, 3.3)
    >>> print(ph.max)
    (4.4, 5.5)
    >>> ph.num_polys
    6
    """
    _fields_ = [
        ('<i', 'file_code'),
        (Point, 'min'),  # nested struct
        (Point, 'max'),  # nested struct
        ('i', 'num_polys')
    ]


###############################################################################
# dealing with a chunk of data.
###############################################################################
class SizedRecord:
    def __init__(self, bytedata):
        self._buffer = memoryview(bytedata)

    @classmethod
    def from_file(cls, f, size_fmt, includes_size=True):
        sz_nbytes = struct.calcsize(size_fmt)
        sz_bytes = f.read(sz_nbytes)
        sz, = struct.unpack(size_fmt, sz_bytes)
        buf = f.read(sz - includes_size * sz_nbytes)
        return cls(buf)

    def iter_as(self, code):
        if isinstance(code, str):
            s = struct.Struct(code)
            for off in range(0, len(self._buffer), s.size):
                yield s.unpack_from(self._buffer, off)
        elif isinstance(code, StructureMeta):
            size = code.struct_size
            for off in range(0, len(self._buffer), size):
                data = self._buffer[off:off+size]
                yield code(data)
