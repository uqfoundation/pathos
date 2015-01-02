#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2015 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE

from pathos.multiprocessing import ProcessingPool as Pool
from pathos.multiprocessing import ThreadingPool as TPool
pool = Pool()
tpool = TPool()

# pickle fails for nested functions
def adder(augend):
  zero = [0]
  def inner(addend):
    return addend+augend+zero[0]
  return inner

# build from inner function
add_me = adder(5)

# build from lambda functions
squ = lambda x:x**2

# test 'dilled' multiprocessing for inner
print "Evaluate 10 items on 2 proc:"
pool.ncpus = 2
print pool
print pool.map(add_me, range(10))
print ''

# test 'dilled' multiprocessing for lambda
print "Evaluate 10 items on 4 proc:"
pool.ncpus = 4
print pool
print pool.map(squ, range(10))
print ''

# test for lambda, but with threads
print "Evaluate 10 items on 4 threads:"
tpool.nthreads = 4
print tpool
print tpool.map(squ, range(10))
print ''

# end of file
