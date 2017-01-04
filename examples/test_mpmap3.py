#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE

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


if __name__ is '__main__':
    from pathos.helpers import freeze_support
    freeze_support()

    from pathos.pools import ProcessPool as Pool
    from pathos.pools import ThreadPool as TPool
    pool = Pool()
    tpool = TPool()

    # test 'dilled' multiprocessing for inner
    print("Evaluate 10 items on 2 proc:")
    pool.ncpus = 2
    print(pool)
    print(pool.map(add_me, range(10)))
    print('')

    # test 'dilled' multiprocessing for lambda
    print("Evaluate 10 items on 4 proc:")
    pool.ncpus = 4
    print(pool)
    print(pool.map(squ, range(10)))
    print('')

    # test for lambda, but with threads
    print("Evaluate 10 items on 4 threads:")
    tpool.nthreads = 4
    print(tpool)
    print(tpool.map(squ, range(10)))
    print('')

# end of file
