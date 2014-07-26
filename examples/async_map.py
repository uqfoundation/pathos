#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE

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
    print pool
    print "y = %s(x1,x2)" % f.__name__
    print "x1 = %s" % str(x[:10])
    print "x2 = %s" % str(x[:10])
    print "I'm sleepy..."
    args = f.func_code.co_argcount
    kwds = f.func_defaults
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
        if not tries: print "Z",
        time.sleep(delay)
        tries += 1
        if (tries % (len(x)*0.01)) == 0:
            print 'z',
            sys.stdout.flush()
        if tries >= maxtries:
            print "TIMEOUT"
            break
    print ""
    y = m.get()
    print "I'm awake"
    print "y = %s" % str(y[:10])



if __name__ == '__main__':
    x = range(500)
    delay = 0.01
    maxtries = 200
    f = busy_add
   #f = busy_squared
   #f = squared

   #from pathos.multiprocessing import ProcessingPool as Pool
   #from pathos.multiprocessing import ThreadingPool as Pool
    from pathos.pp import ParallelPythonPool as Pool

    pool = Pool(nodes=4)
    test_ready( pool, f, maxtries, delay )


# EOF
