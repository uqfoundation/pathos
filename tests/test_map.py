#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE

def busy_add(x,y, delay):
    for n in range(x):
       x += n
    for n in range(y):
       y -= n
    import time
    time.sleep(delay)
    return x + y

if __name__ == '__main__':
    import time
    delay = 0.1
    items = 100
    print "CONFIG: delay = %s" % delay
    print "CONFIG: items = %s" % items
    print ""

    _x = range(-items/2,items/2,2)
    _y = range(len(_x))
    _d = [delay]*len(_x)

    from pathos.python import PythonSerial as PS
    basic = PS()
    print basic
    start = time.time()
    res = basic.map(busy_add, _x, _y, _d)
    print "time to queue:", time.time() - start
    start = time.time()
    _basic = list(res)
    print "time to results:", time.time() - start
    print ""

    from pathos.pp import ParallelPythonPool as PPP
    #from pathos.pp import stats
    pp_pool = PPP(4, servers=('localhost:5653','localhost:2414'))
    print pp_pool
    start = time.time()
    res = pp_pool.map(busy_add, _x, _y, _d)
    print "time to queue:", time.time() - start
    start = time.time()
    _pp_pool = list(res)
    print "time to results:", time.time() - start
    #print stats()

    assert _basic == _pp_pool
    print ""

    from pathos.multiprocessing import ProcessingPool as MPP
    mp_pool = MPP(4)
    print mp_pool
    start = time.time()
    res = mp_pool.map(busy_add, _x, _y, _d)
    print "time to queue:", time.time() - start
    start = time.time()
    _mp_pool = list(res)
    print "time to results:", time.time() - start

    assert _basic == _mp_pool
    print ""


# EOF
