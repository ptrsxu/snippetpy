#!/usr/bin/env python

def no_new_attrs(wrapped_setattr):
    def __setattr__(self, name, attr):
        if hasattr(self, name):
            wrapped_setattr(self, name, attr)
        else:
            raise AttributeError("Cannot add new attributes to %s" % self)
    return __setattr__

class NoNewAttrs(object):
    """A class whose subclassses cannot add new attributes dynamically.

    Example:
    >>> class Test(NoNewAttrs):
    ...     attr1 = ''
    ...     attr2 = ''
    ...     def __init__(self, para1, para2):
    ...         self.attr1 = para1
    ...         self.attr2 = para2
    ...     def __repr__(self):
    ...         return 'Test(%s, %s)' % (self.attr1, self.attr2)
    ...
    >>> t = Test('hello', 'world')
    >>> t.attr1
    'hello'
    >>> try:
    ...     t.other = 4
    ... except AttributeError:
    ...     print('Got AttributeError')
    ...
    Got AttributeError
    >>> Test.attr1
    ''
    >>> try:
    ...     Test.other = 4
    ... except AttributeError:
    ...     print('Got AttributeError')
    ...
    Got AttributeError
    """
    # This make sure that the instances cannot add new attributes.
    __setattr__ = no_new_attrs(object.__setattr__)

    # This make sure that the class cannot add new attributes.
    class __metaclass__(type):
        __setattr__ = no_new_attrs(type.__setattr__)
