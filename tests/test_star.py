#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE

import time, random

x = range(18)
delay = 0.01
items = 20
maxtries = 20


def busy_add(x,y, delay=0.01):
    for n in range(x):
       x += n
    for n in range(y):
       y -= n
    time.sleep(delay)
    return x + y

def busy_squared(x, delay=True):
    if delay is True: delay = random.random()
    if not delay: delay = 0
    time.sleep(2*delay)
    return x*x

def squared(x):
    return x*x

def quad_factory(a=1, b=1, c=0):
    def quad(x):
        return a*x**2 + b*x + c
    return quad

square_plus_one = quad_factory(2,0,1)

x2 = map(squared, x)


def test_sanity(pool, verbose=False):
    if verbose:
        print pool
        print "x: %s\n" % str(x)

        print pool.map.__name__
    # blocking map
    start = time.time()
    res = pool.map(squared, x)
    end = time.time() - start
    assert res == x2
    if verbose:
        print "time to results:", end
        print "y: %s\n" % str(res)

        print pool.imap.__name__
    # iterative map
    start = time.time()
    res = pool.imap(squared, x)
    fin = time.time() - start
    # get result from iterator
    start = time.time()
    res = list(res)
    end = time.time() - start
    assert res == x2
    if verbose:
        print "time to queue:", fin
        print "time to results:", end
        print "y: %s\n" % str(res)

        print pool.amap.__name__
    # asyncronous map
    start = time.time()
    res = pool.amap(squared, x)
    fin = time.time() - start
    # get result from result object
    start = time.time()
    res = res.get()
    end = time.time() - start
    assert res == x2
    if verbose:
        print "time to queue:", fin
        print "time to results:", end
        print "y: %s\n" % str(res)


def test2(pool, items=4, delay=0):
    _x = range(-items/2,items/2,2)
    _y = range(len(_x))
    _d = [delay]*len(_x)
    _z = [0]*len(_x)

   #print map
    res1 = map(squared, _x)
    res2 = map(busy_add, _x, _y, _z)

   #print pool.map
    _res1 = pool.map(busy_squared, _x, _d)
    _res2 = pool.map(busy_add, _x, _y, _d)
    assert _res1 == res1
    assert _res2 == res2

   #print pool.imap
    _res1 = pool.imap(busy_squared, _x, _d)
    _res2 = pool.imap(busy_add, _x, _y, _d)
    assert list(_res1) == res1
    assert list(_res2) == res2

   #print pool.uimap
   #_res1 = pool.uimap(busy_squared, _x, _d)
   #_res2 = pool.uimap(busy_add, _x, _y, _d)
   #assert sorted(_res1) == sorted(res1)
   #assert sorted(_res2) == sorted(res2)

   #print pool.amap
    _res1 = pool.amap(busy_squared, _x, _d)
    _res2 = pool.amap(busy_add, _x, _y, _d)
    assert _res1.get() == res1
    assert _res2.get() == res2
   #print ""


def test3(pool, verbose=False): # test a function that should fail in pickle
    if verbose:
        print pool
        print "x: %s\n" % str(x)

        print pool.map.__name__
   #start = time.time()
    try:
        res = pool.map(square_plus_one, x)
    except:
        assert False # should use a smarter test here...
   #end = time.time() - start
   #    print "time to results:", end
        print "y: %s\n" % str(res)
    assert True


def test4(pool, maxtries, delay):
    print pool
   #m = pool.amap(busy_squared, x)
    m = pool.amap(busy_add, x, x)

  # print m.ready()
  # print m.wait(0) 
    tries = 0
    while not m.ready():
        time.sleep(delay)
        tries += 1
        print "TRY: %s" % tries
        if tries >= maxtries:
            print "TIMEOUT"
            break
   #print m.ready()
#   print m.get(0)
    print m.get()



if __name__ == '__main__':
    from pathos.multiprocessing import ProcessingPool as Pool
   #from pathos.multiprocessing import ThreadingPool as Pool
   #from pathos.pp import ParallelPythonPool as Pool

    pool = Pool(nodes=4)
    test_sanity( pool )
    test2( pool, items, delay )
    test3( pool )
    test4( pool, maxtries, delay )


# EOF
