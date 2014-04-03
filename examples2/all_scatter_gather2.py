#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
"""example: using the same code with different parallel backends

Requires: development version of pathos, pyina
  http://pypi.python.org/pypi/pathos
  http://pypi.python.org/pypi/pyina

Run with:
>$ python all_scatter_gather2.py
"""

import numpy as np
from pyina.launchers import Mpi as MpiPool
from pathos.multiprocessing import ProcessingPool
from pathos.pp import ParallelPythonPool
nodes = 2; N = 3

# the sin of the difference of two numbers
def sin_diff(x, xp):
  """d = sin(x - x')"""
  from numpy import sin
  return sin(x - xp)


# print the input to screen
x = np.arange(N * nodes, dtype=np.float64)
xp = np.arange(N * nodes, dtype=np.float64)[::-1]
print("Input: %s\n" % x)

# map sin_diff to the workers, then print to screen
print("Running serial python ...")
y = map(sin_diff, x, xp)
print("Output: %s\n" % np.asarray(y))


# map sin_diff to the workers, then print to screen
print("Running mpi4py on %d cores..." % nodes)
y = MpiPool(nodes).map(sin_diff, x, xp)
print("Output: %s\n" % np.asarray(y))


# map sin_diff to the workers, then print to screen
print("Running multiprocesing on %d processors..." % nodes)
y = ProcessingPool(nodes).map(sin_diff, x, xp)
print("Output: %s\n" % np.asarray(y))


# map sin_diff to the workers, then print to screen
print("Running parallelpython on %d cpus..." % nodes)
y = ParallelPythonPool(nodes).map(sin_diff, x, xp)
print("Output: %s\n" % np.asarray(y))

# EOF
