#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
from python cookbook 3nd edition.
"""
import types

################################################################################
# 基于描述符的装饰器实现 (PY2-new-object & PY3)
################################################################################
class multimethods(object):
    def __init__(self, func):
        self._methods = {}
        self.__name__ = func.__name__
        self._default = func

    def match(self, *types):
        def wrapper(func):
            self._methods[tuple(types)] = func
            return self
        return wrapper

    def __call__(self, *args):
        types = tuple([type(e) for e in args[1:]])
        if types:
            return self._methods[types](*args)
        else:
            return self._default(*args)

    def __get__(self, instance, cls):
        if instance:
            return types.MethodType(self, instance)
        else:
            return self


class User(object):
    def __init__(self, name):
        self._name = name

    @multimethods
    def info(self):
        return "I am " + self._name

    @info.match(int)
    def info(self, age):
        return "I am " + self._name + \
            " and I am " + str(age) + " years old"

    @info.match(str)
    def info(self, job):
        return "I am " + self._name + " and I am a " + job


def main1():
    user = User('Peter')
    print(user.info())
    print(user.info(3))
    print(user.info('Programmer'))


################################################################################
# 基于描述符和元类的实现 (PY3)
# 尽量简单的实现版本，只为说明，未包含所有可能的待处理情况
# 更多细节可以参考 Python Cookbook V3
#   9.20. Implementing Multiple Dispatch with Function Annotations
################################################################################
from inspect import signature
from collections import Callable
import types

class MultiMethods:
    def __init__(self, func):
        self._methods = {}
        self.register(func)

    def register(self, func):
        sig = signature(func)
        # 需要把 self 去掉，self 的参数信息为空(inspect._empty)
        annos = tuple(v.annotation for k, v in sig.parameters.items()
                      if k != "self")
        self._methods[annos] = func
        return self

    def __call__(self, *args):
        # 同理去掉调用的对象本身(传给方法的 self)
        types = tuple(type(i) for i in args[1:])
        m = self._methods.get(types, None)
        if m:
            # 下面的 __get__ 保证了此句可执行
            return m(*args)
        else:
            raise NotImplementedError("%s" % str(args))

    # 传给上面 __call__ 的参数 args 中是不带
    # self 的，但保存到 _methods 中的方法对象
    # 却是需要带 self 进行调用，下面的语句将
    # MultiMethods 对象伪装成其调用者的实例方法
    def __get__(self, instance, cls):
        if instance:
            return types.MethodType(self, instance)
        else:
            return self

class MultiDict(dict):
    def __setitem__(self, k, v):
        if not isinstance(v, Callable):
            super().__setitem__(k, v)
            return

        if k in self:
            oldv = super().__getitem__(k)
            if isinstance(oldv, MultiMethods):
                super().__setitem__(k, oldv.register(v))
            else:
                newv = MultiMethods(oldv)
                super().__setitem__(k, newv.register(v))
        else:
            super().__setitem__(k, v)


class PolymMethods(type):
    def __new__(cls, clsname, bases, clsdict):
        return type.__new__(cls, clsname, bases, dict(clsdict))

    @classmethod
    def __prepare__(cls, clsname, bases):
        return MultiDict()


class User2(metaclass=PolymMethods):
    gogogo = "ou lay ou lay ou lay"
    def __init__(self, name):
        self._name = name

    def info(self):
        return "I am " + self._name

    def info(self, age: int):
        return "I am " + self._name + \
            " and I am " + str(age) + " years old"

    def info(self, job: str):
        return "I am " + self._name + " and I am a " + job

    def olay(self):
        return self.gogogo


def main2():
    user2 = User2('Peter')
    print(user2.info())
    print(user2.info(3))
    print(user2.info('Programmer'))
    print(user2.olay())


if __name__ == '__main__':
    main1()
    print('--------------------------------------------------')
    main2()
