"""
A colleciton of snippet for python code about advanced feature metaclass.
"""

class AutoGetter(type):
    """A metaclass that auto finish the strings in ``__slots__`` that
    starts with ``_autoget`` into a getter method.

    Example:
    >>> class TestAutoGetter(object):
    ...     __metaclass__ = AutoGetter
    ...     __slots__ = ('_get_name', '_get_age')
    ...     def __init__(self, a, b):
    ...         TestAutoGetter._get_name = a
    ...         TestAutoGetter._get_age = b
    ...
    >>> t = TestAutoGetter('peter', 3)
    >>> t.get_name()
    'peter'
    >>> t.get_age()
    3
    """
    def __new__(cls, name, bases, classdict):
        for attr in classdict.get('__slots__', ()):
            if attr.startswith('_get'):
                def getter(self, attr=attr):
                    return getattr(self, attr)
                classdict['get_' + attr[5:]] = getter
        return type.__new__(cls, name, bases, classdict)
