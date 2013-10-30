#!/usr/bin/env python
# -*- coding: UTF-8 -*-

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


class InterfaceOmission(TypeError):
    """A kind of error that a class missed to implement a interface."""
    pass


class MetaInterfaceChecker(type):
    """A metaclass checks if a class implements specified interfaces.

    If we want to check if a class implements some specifed interfaces,
    we need to specify the ``__metaclass__`` of the class to this
    meta class, and specify the ``__implements__`` of the class to
    a tuple that includes all the interfaces we want to check.
    """
    def __init__(cls, classname, bases, classdict):
        super(MetaInterfaceChecker, cls).__init__(classname,
                bases, classdict)
        defined = set(dir(cls))
        for interface in cls.__implements__:
            checklist = set(dir(interface))
            if not checklist.issubset(defined):
                raise InterfaceOmission, list(checklist - defined)


from functools import wraps, update_wrapper
def make_chainable(func):
    # @wraps(func)
    # Notice that we cannot use ``@wraps`` for a class method.
    def chainable_wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        return self
    return chainable_wrapper

class MetaChainable(type):
    def __new__(mcl, classname, bases, classdict):
        for base in bases:
            if not isinstance(base, MetaChainable):
                for mutator in classdict['__mutators__']:
                    if mutator not in classdict:
                        classdict[mutator] = make_chainable(getattr(base,
                            mutator))
                break
        return super(MetaChainable, mcl).__new__(mcl, classname, bases,
                classdict)


# Here must be an old style class, donnot inherit from object.
class Chainable:
    """A class that makes specifed operations of an object chainable.

    We just need to specify the ``__mutators__`` of the class by a tuple
    that contains all the operations we need to be chainable.

    Example:
    >>> class ChainableList(Chainable, list):
    ...     __mutators__ = 'sort reverse extend'.split()
    ...
    >>> print(''.join(ChainableList('hello').reverse().extend('world')))
    ollehworld
    """
    __metaclass__ = MetaChainable


import weakref
class MetaInstanceTracker(type):
    """A meta class that insures it's classes tracing instances."""
    def __init__(cls, classname, bases, classdict):
        super(MetaInstanceTracker, cls).__init__(classname, bases, classdict)
        cls.__instance_refs__ = []

    def __instances__(cls):
        """Returns al alive instances of cls."""
        # ref and obj alive.
        instances = [(r, r()) for r in cls.__instance_refs__ if r() is not None]
        cls.__instance_refs__ = [r for (r, o) in instances]
        return [o for (r, o) in instances]

    def __call__(cls, *args, **kwargs):
        """Generate and weakref a instance."""
        instance = super(MetaInstanceTracker, cls).__call__(*args, **kwargs)
        cls.__instance_refs__.append(weakref.ref(instance))
        return instance


# Remember donnot inherit from object.
class InstanceTracker:
    """A class that has an ability of tracking it's instances.

    Example:
    >>> a = InstanceTracker()
    >>> b = InstanceTracker()
    >>> c = InstanceTracker()
    >>> len(InstanceTracker.__instance_refs__)
    3
    >>> class TestInstanceTracker(InstanceTracker):
    ...     pass
    ...
    >>> d = TestInstanceTracker()
    >>> e = TestInstanceTracker()
    >>> len(InstanceTracker.__instance_refs__)
    3
    >>> len(TestInstanceTracker.__instance_refs__)
    2
    """
    __metaclass__=MetaInstanceTracker


import inspect
class MetaAutoReloader(MetaInstanceTracker):
    """A meta class, classes uses this meta class would have their old
    instances and subclasses refreshed when the classes is reloaded.
    """
    def __init__(cls, classname, bases, classdict):
        updater = classdict.pop('__update__', None)
        super(MetaAutoReloader, cls).__init__(classname, bases, classdict)
        # check our caller's locals and globals in stack frame
        f = inspect.currentframe().f_back
        for d in (f.f_locals, f.f_globals):
            if classname in d:
                old_class = d[classname]
                #if not isinstance(old_class, cls):
                if not isinstance(old_class, cls.__class__):
                   continue
                for instance in old_class.__instances__():
                    instance.__class__ = cls
                    if updater:
                        updater(instance)
                    cls.__instance_refs__.append(weakref.ref(instance))
                for subclass in old_class.__subclasses__():
                    bases = list(subclass.__bases__)
                    bases[bases.index(old_class)] = cls
                    subclass.__bases__ = tuple(bases)
                    for instance in subclass.__instances__():
                        if updater:
                            updater(instance)
                break


class AutoReloader:
    """The subclasses of AutoGetter will have the ability of auto refreshing.

    Example:
    >>> class Foo(AutoReloader):
    ...     def __init__(self, para=99):
    ...         self.old = para
    ...
    >>> class Bar(Foo): pass
    ...
    >>> f = Foo()
    >>> b = Bar()
    >>> len(Foo.__instance_refs__)
    1
    >>> len(Bar.__instance_refs__)
    1
    >>> class Foo(AutoReloader):
    ...     def __init__(self, para=66):
    ...         self.new = para + 1
    ...     def __update__(self):
    ...         self.new = self.old + 100
    ...         del self.old
    ...     def meth(self, para):
    ...         print(para, self.new)
    ...
    >>> len(Foo.__instance_refs__)
    1
    >>> f.meth(123)
    (123, 199)
    >>> b.meth(456)
    (456, 199)
    >>> Bar().meth(999)
    (999, 67)
    """
    __metaclass__=MetaAutoReloader
