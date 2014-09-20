#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""from python cookbook 2nd edition."""

def curry(f, *a, **kw):
    """ showing curry technology """
    def curried(*more_a, **more_kw):
        # named args in more_kw replaced that in kw
        # return f(*(a + more_a), **dict(kw, **more_kw))
        # named args in kw replaced that in more_kw
        return f(*(a + more_a), **dict(more_kw, **kw))
    return curried

def compose(f, g, *args_for_f, **kwargs_for_f):
    """ compose function: compose(f, g, x)(y) = f(g(y), x) """
    def fg(*args_for_g, **kwargs_for_g):
        return f(g(*args_for_g, **kwargs_for_g), *args_for_f, **kwargs_for_f)
    return fg

def mcompose(f, g, *args_for_f, **kwargs_for_f):
    """ compose function: compose(f, g, x)(y) = f(*g(y), x) """
    def fg(*args_for_g, **kwargs_for_g):
        mid = g(*args_for_g, **kwargs_for_g)
        if not isinstance(mid, tuple):
            mid = (mid,)
        return f(*(args_for_f + mid), **kwargs_for_f)
    return fg

def main():
    def personinfo(*a, **kw):
        print "his info: ", a, kw
        return 'hero', 'winner'

    print "-------------------- Curry -----------------------"
    print "old:"
    personinfo('peter', '27', city = 'Beijing', gender = 'M')
    print "new:"
    newpersoninfo = curry(personinfo, 'CEO', city = 'Wuhan', job = 'coder')
    newpersoninfo('peter', '27', city = 'Beijing', gender = 'M')

    print "-------------------- Compose ---------------------"
    def allinfo(*a, **kw):
        print "allinfo: ", a, kw

    print "old:"
    personinfo('peter', '27', city = 'Beijing', gender = 'M')
    print "new:"
    compose(allinfo, personinfo, 'dota', 'python', lover = 'nano')('peter', '27', city = 'Beijing', gender = 'M')

    print "-------------------- Compose ---------------------"
    parts = compose(' '.join, dir)
    print parts('__builtins__')

    print "-------------------- MCompose ---------------------"
    print "old:"
    personinfo('peter', '27', city = 'Beijing', gender = 'M')
    print "new:"
    mcompose(allinfo, personinfo, 'dota', 'python', lover = 'nano')('peter', '27', city = 'Beijing', gender = 'M')

if __name__=="__main__":
    main()
