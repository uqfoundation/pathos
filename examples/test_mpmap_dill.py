#!/usr/bin/env python

from pathos.multiprocessing import Pool
import dill
import pickle #FIXME: multiprocessing needs cPickle + copy_reg
pool = Pool()

# pickle fails for nested functions
def adder(augend):
  zero = [0]
  def inner(addend):
    return addend+augend+zero[0]
  return inner

# test the pickle-ability of inner function
add_me = adder(5)
pinner = pickle.dumps(add_me)
p_add_me = pickle.loads(pinner)
assert add_me(10) == p_add_me(10)

# pickle fails for lambda functions
squ = lambda x:x**2

# test the pickle-ability of inner function
psqu = pickle.dumps(squ)
p_squ = pickle.loads(psqu)
assert squ(10) == p_squ(10)

# if pickle works, then multiprocessing should too
print "Evaluate 10 items on 2 proc:"
pool.ncpus = 2
p_res = pool.map(add_me, range(10))
print '%s' % p_res
print ''

# if pickle works, then multiprocessing should too
print "Evaluate 10 items on 4 proc:"
pool.ncpus = 4
p2res = pool.map(squ, range(10))
print '%s' % p2res
print ''

# end of file
