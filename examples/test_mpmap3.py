#!/usr/bin/env python

from pathos.mp_map import mp_map

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
print mp_map(add_me, range(10), nproc=2)
print ''

# test 'dilled' multiprocessing for lambda
print "Evaluate 10 items on 4 proc:"
print mp_map(squ, range(10), nproc=4)
print ''

'''
# test for lambda, but with threads
print "Evaluate 10 items on 4 threads:"
print mp_map(squ, range(10), nproc=4, threads=True)
print ''
'''

# end of file
