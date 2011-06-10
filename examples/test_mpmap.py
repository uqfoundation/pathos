#
# A test of `processing.Pool` class
#

from pathos.mp_map import mp_map

import time, random, sys

#
# Functions used by test code
#

def pow3(x):
    return x**3

#
# Test code
#

def test():
    
    N = 100000
    print 'def pow3(x): return x**3'
    
    t = time.time()
    A = map(pow3, xrange(N))
    print 'map(pow3, xrange(%d)):\n\t%s seconds' % \
          (N, time.time() - t)
    
    t = time.time()
    B = mp_map(pow3, xrange(N))
    print 'mp_map(pow3, xrange(%d)):\n\t%s seconds' % \
          (N, time.time() - t)

    t = time.time()
    D = mp_map(pow3, xrange(N), nproc=4)
    print 'mp_map(pow3, xrange(%d), nproc=4):\n\t%s seconds' % \
          (N, time.time() - t)

    t = time.time()
    C = mp_map(pow3, xrange(N), type='ordered', chunksize=N//8)
    print "mp_map(pow3, xrange(%d), type='ordered', chunksize=%d):\n\t%s" \
          ' seconds' % (N, N//8, time.time() - t)
    
    assert A == B == C == D, (len(A), len(B), len(C), len(D))


    
if __name__ == '__main__':
    test()

