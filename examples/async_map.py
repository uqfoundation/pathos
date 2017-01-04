#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE

from __future__ import print_function
import time
import sys

def busy_add(x,y, delay=0.01):
    for n in range(x):
       x += n
    for n in range(y):
       y -= n
    time.sleep(delay)
    return x + y

def busy_squared(x):
    import random
    time.sleep(0.01*random.random())
    return x*x

def squared(x):
    return x*x

def quad_factory(a=1, b=1, c=0):
    def quad(x):
        return a*x**2 + b*x + c
    return quad

square_plus_one = quad_factory(2,0,1)

 
def test_ready(pool, f, maxtries, delay):
    print(pool)
    print("y = %s(x1,x2)" % f.__name__)
    print("x1 = %s" % str(x[:10]))
    print("x2 = %s" % str(x[:10]))
    print("I'm sleepy...")
    args = (getattr(f,'__code__',None) or getattr(f,'func_code')).co_argcount
    kwds = getattr(f,'__defaults__',None) or getattr(f,'func_defaults')
    args = args - len(kwds) if kwds else args
    if args == 1:
        m = pool.amap(f, x)
    elif args == 2:
        m = pool.amap(f, x, x)
    else:
        msg = 'takes a function of 1 or 2 required arguments, %s given' % args
        raise NotImplementedError(msg)

    tries = 0
    while not m.ready():
        if not tries: print("Z", end='')
        time.sleep(delay)
        tries += 1
        if (tries % (len(x)*0.01)) == 0:
            print('z', end='')
            sys.stdout.flush()
        if tries >= maxtries:
            print("TIMEOUT")
            break
    print("")
    y = m.get()
    print("I'm awake")
    print("y = %s" % str(y[:10]))



if __name__ == '__main__':
    x = list(range(500))
    delay = 0.01
    maxtries = 200
    f = busy_add
   #f = busy_squared
   #f = squared

   #from pathos.pools import ProcessPool as Pool
   #from pathos.pools import ThreadPool as Pool
    from pathos.pools import ParallelPool as Pool
   #from pathos.helpers import freeze_support
   #freeze_support()

    pool = Pool(nodes=4)
    test_ready( pool, f, maxtries, delay )


# EOF
