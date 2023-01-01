#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE

import dill
import pickle #XXX: multiprocessing needs cPickle + copy_reg

dumps = pickle._dumps
loads = pickle._loads

# pickle fails for nested functions
def adder(augend):
  zero = [0]
  def inner(addend):
    return addend+augend+zero[0]
  return inner

# test the pickle-ability of inner function
add_me = adder(5)
pinner = dumps(add_me)
p_add_me = loads(pinner)
assert add_me(10) == p_add_me(10)

# pickle fails for lambda functions
squ = lambda x:x**2

# test the pickle-ability of inner function
psqu = dumps(squ)
p_squ = loads(psqu)
assert squ(10) == p_squ(10)


if __name__ == '__main__':
    from pathos.helpers import freeze_support
    freeze_support()

    from pathos.pools import _ProcessPool as Pool
    pool = Pool()

    # if pickle works, then multiprocessing should too
    print("Evaluate 10 items on 2 proc:")
    pool.ncpus = 2
    p_res = pool.map(add_me, range(10))
    print(pool)
    print('%s' % p_res)
    print('')

    # if pickle works, then multiprocessing should too
    print("Evaluate 10 items on 4 proc:")
    pool.ncpus = 4
    p2res = pool.map(squ, range(10))
    print(pool)
    print('%s' % p2res)
    print('')

    # shutdown the pool
    pool.close()

# end of file
