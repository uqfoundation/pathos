#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE
"""example: parallelism in python with mp4py

Run with:
> $ mpirun -np 2 scatter_gather.py
"""

import numpy as np

from mpi4py import MPI
comm = MPI.COMM_WORLD
nodes = comm.size #2
my_N = 3
N = my_N * nodes

# a print function that prints only to rank 0
def pprint(str="", end="\n", comm=comm):
    """Print for MPI parallel programs: Only rank 0 prints *str*."""
    if comm.rank == 0:
        print(str, end=end)

# set up the target arrays
if comm.rank == 0:
    x = np.arange(N, dtype=np.float64)
else:
    x = np.empty(N, dtype=np.float64)

my_x = np.empty(my_N, dtype=np.float64)

# scatter data into arrays on each node
comm.Scatter( [x, MPI.DOUBLE], [my_x, MPI.DOUBLE] )

# print the input to screen
pprint("Input:")
for r in range(nodes):
    if comm.rank == r:
        print(" [node %d] %s" % (comm.rank, my_x))
    comm.Barrier()

# take the sin squared of all data
pprint("Running on %d cores..." % nodes)
my_x = np.sin(my_x)**2

# gather data into the head node
comm.Gather( [my_x, MPI.DOUBLE], [x, MPI.DOUBLE] )

# print the ouput to screen
pprint("Output:\n %s" % x)

# EOF
