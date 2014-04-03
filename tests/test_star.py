#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE

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


def test1(pool):
    print pool
    print "x: %s\n" % str(x)

    print pool.map.__name__
    start = time.time()
    res = pool.map(squared, x)
    print "time to results:", time.time() - start
    print "y: %s\n" % str(res)

    print pool.imap.__name__
    start = time.time()
    res = pool.imap(squared, x)
    print "time to queue:", time.time() - start
    start = time.time()
    res = list(res)
    print "time to results:", time.time() - start
    print "y: %s\n" % str(res)

   #print pool.uimap.__name__
   #start = time.time()
   #res = pool.uimap(squared, x)
   #print "time to queue:", time.time() - start
   #start = time.time()
   #res = list(res)
   #print "time to results:", time.time() - start
   #print "y: %s\n" % str(res)

    print pool.amap.__name__
    start = time.time()
    res = pool.amap(squared, x)
    print "time to queue:", time.time() - start
    start = time.time()
    res = res.get()
    print "time to results:", time.time() - start
    print "y: %s\n" % str(res)


def test2(pool, items=4, delay=0):
    _x = range(-items/2,items/2,2)
    _y = range(len(_x))
    _d = [delay]*len(_x)

    print map
    res1 = map(busy_squared, _x)
    res2 = map(busy_add, _x, _y, _d)

    print pool.map
    _res1 = pool.map(busy_squared, _x)
    _res2 = pool.map(busy_add, _x, _y, _d)
    assert _res1 == res1
    assert _res2 == res2

    print pool.imap
    _res1 = pool.imap(busy_squared, _x)
    _res2 = pool.imap(busy_add, _x, _y, _d)
    assert list(_res1) == res1
    assert list(_res2) == res2

   #print pool.uimap
   #_res1 = pool.uimap(busy_squared, _x)
   #_res2 = pool.uimap(busy_add, _x, _y, _d)
   #assert sorted(_res1) == sorted(res1)
   #assert sorted(_res2) == sorted(res2)

    print pool.amap
    _res1 = pool.amap(busy_squared, _x)
    _res2 = pool.amap(busy_add, _x, _y, _d)
    assert _res1.get() == res1
    assert _res2.get() == res2
    print ""


def test3(pool): # test against a function that should fail in pickle
    print pool
    print "x: %s\n" % str(x)

    print pool.map.__name__
    start = time.time()
    res = pool.map(square_plus_one, x)
    print "time to results:", time.time() - start
    print "y: %s\n" % str(res)


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
    import time
    x = range(18)
    delay = 0.01
    items = 20
    maxtries = 20

    from pathos.multiprocessing import ProcessingPool as Pool; skip = False
   #from pathos.multiprocessing import ThreadingPool as Pool; skip = False
   #from pathos.pp import ParallelPythonPool as Pool; skip = True

    pool = Pool(nodes=4)
    test1( pool )
    test2( pool, items, delay )
    if not skip: test3( pool ) #XXX: fails for pathos.pp
    test4( pool, maxtries, delay )


# EOF
