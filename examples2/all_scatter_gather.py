#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
"""example: using the same code with different parallel backends

Requires: development version of pathos, pyina
  http://pypi.python.org/pypi/pathos
  http://pypi.python.org/pypi/pyina

Run with:
>$ python all_scatter_gather.py
"""

import numpy as np
from pathos.helpers import freeze_support
from pathos.pools import ProcessPool
from pathos.pools import ParallelPool
from pathos.pools import ThreadPool
try:
    from pyina.launchers import Mpi as MpiPool
    HAS_PYINA = True
except ImportError:
    HAS_PYINA = False

nodes = 2; N = 3

# take sin squared of all data
def sin2(xi):
    """sin squared of all data"""
    import numpy as np
    return np.sin(xi)**2


if __name__ == '__main__':
    # ensure properly forks on Windows
    freeze_support()

    # print the input to screen
    x = np.arange(N * nodes, dtype=np.float64)
    print("Input: %s\n" % x)


    # run sin2 in series, then print to screen
    print("Running serial python ...")
    y = list(map(sin2, x))
    print("Output: %s\n" % np.asarray(y))


    if HAS_PYINA:
        # map sin2 to the workers, then print to screen
        print("Running mpi4py on %d cores..." % nodes)
        y = MpiPool(nodes).map(sin2, x)
        print("Output: %s\n" % np.asarray(y))


    # map sin2 to the workers, then print to screen
    print("Running multiprocesing on %d processors..." % nodes)
    y = ProcessPool(nodes).map(sin2, x)
    print("Output: %s\n" % np.asarray(y))


    # map sin2 to the workers, then print to screen
    print("Running multiprocesing on %d threads..." % nodes)
    y = ThreadPool(nodes).map(sin2, x)
    print("Output: %s\n" % np.asarray(y))


    # map sin2 to the workers, then print to screen
    print("Running parallelpython on %d cpus..." % nodes)
    y = ParallelPool(nodes).map(sin2, x)
    print("Output: %s\n" % np.asarray(y))

# EOF
