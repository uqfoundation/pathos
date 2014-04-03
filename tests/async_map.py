#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE

import sys

def busy_add(x,y, delay=0.01):
    for n in range(x):
       x += n
    for n in range(y):
       y -= n
    import time
    time.sleep(delay)
    return x + y

def busy_squared(x):
    import time, random
    time.sleep(2*random.random())
    return x*x

def squared(x):
    return x*x

def quad_factory(a=1, b=1, c=0):
    def quad(x):
        return a*x**2 + b*x + c
    return quad

square_plus_one = quad_factory(2,0,1)


def test4(pool, maxtries, delay):
    print pool
    f = busy_add
    print "y = %s(x1,x2)" % f.__name__
    print "x1 = %s" % str(x[:10])
    print "x2 = %s" % str(x[:10])
    print "I'm sleepy..."
   #m = pool.amap(f, x)
    m = pool.amap(f, x, x)

    tries = 0
    print "Z",
    while not m.ready():
        time.sleep(delay)
        tries += 1
       #print "TRY: %s" % tries
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
    import time
    x = range(500)
    delay = 0.01
    maxtries = 200

    from pathos.multiprocessing import ProcessingPool as Pool; skip = False
   #from pathos.multiprocessing import ThreadingPool as Pool; skip = False
   #from pathos.pp import ParallelPythonPool as Pool; skip = True

    pool = Pool(nodes=4)
    test4( pool, maxtries, delay )


# EOF
