#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE
"""example: using the same code with different parallel backends

Requires: development version of pathos, pyina
  http://pypi.python.org/pypi/pathos
  http://pypi.python.org/pypi/pyina

Run with:
>$ python all_scatter_gather2.py
"""

import numpy as np
from pathos.helpers import freeze_support, shutdown
from pathos.pools import ProcessPool
from pathos.pools import ParallelPool
from pathos.pools import ThreadPool
try:
    from pyina.launchers import Mpi as MpiPool
    HAS_PYINA = True
except ImportError:
    HAS_PYINA = False

nodes = 2; N = 3

# the sin of the difference of two numbers
def sin_diff(x, xp):
  """d = sin(x - x')"""
  from numpy import sin
  return sin(x - xp)


if __name__ == '__main__':
    # ensure properly forks on Windows
    freeze_support()

    # print the input to screen
    x = np.arange(N * nodes, dtype=np.float64)
    xp = np.arange(N * nodes, dtype=np.float64)[::-1]
    print("Input: %s\n" % x)

    # map sin_diff to the workers, then print to screen
    print("Running serial python ...")
    y = list(map(sin_diff, x, xp))
    print("Output: %s\n" % np.asarray(y))

    if HAS_PYINA:
        # map sin_diff to the workers, then print to screen
        print("Running mpi4py on %d cores..." % nodes)
        y = MpiPool(nodes).map(sin_diff, x, xp)
        print("Output: %s\n" % np.asarray(y))

    # map sin_diff to the workers, then print to screen
    print("Running multiprocesing on %d processors..." % nodes)
    y = ProcessPool(nodes).map(sin_diff, x, xp)
    print("Output: %s\n" % np.asarray(y))

    # map sin_diff to the workers, then print to screen
    print("Running multiprocesing on %d threads..." % nodes)
    y = ThreadPool(nodes).map(sin_diff, x, xp)
    print("Output: %s\n" % np.asarray(y))

    # map sin_diff to the workers, then print to screen
    print("Running parallelpython on %d cpus..." % nodes)
    y = ParallelPool(nodes).map(sin_diff, x, xp)
    print("Output: %s\n" % np.asarray(y))

    # ensure all pools shutdown
    shutdown()

# EOF
