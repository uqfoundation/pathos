#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
"""
Solve Nth-order Chebyshev polynomial coefficients with Powell's method.
Launch optimizers with mpi4py's map.

Requires: development version of mystic, pyina
  http://pypi.python.org/pypi/mystic
  http://pypi.python.org/pypi/pyina
"""

def optimize(solver, mapper, nodes, target='rosen', **kwds):
    if target == 'rosen': # 3d-rosenbrock
        ndim = 3
        actual_coeffs = [1.0] * ndim
        pprint = list
    else: # 4th-order chebyshev
        from poly import chebyshev4coeffs as actual_coeffs
        ndim = len(actual_coeffs)
        from mystic.math import poly1d as pprint

    # number of trials
    N = nodes
    print("Number of trials: %s" % N)
    print("===============")

    # initial guess
    import random
    x0 = [[random.uniform(-100,100) for i in range(ndim)] for i in range(N)]

    # minimize the function
    results = mapper(nodes).map(solver, x0)

    # find the results with the lowest energy
    from optimize_helper import best_results
    solution = best_results(results)

    print("===============")
    print("Actual params:\n %s" % pprint(actual_coeffs))
    print("Solved params:\n %s" % pprint(solution[0]))
    print("Function value: %s" % solution[1])
    print("Total function evals: %s" % solution[4])
    return 


# build the solver-model pairs
def powell_chebyshev(x0, *args, **kwds):
    # Powell's Directonal solver
    from optimize_helper import fmin_powell as the_solver
    # Chebyshev cost function
    from poly import chebyshev4cost as the_model
    return the_solver(the_model, x0, monitor=False, *args, **kwds)

# get the map functions
from pyina.launchers import Mpi as mpipool


if __name__ == '__main__':
    target = 'cheby'
    print("Function: %s" % target)
    print("Solver: %s" % 'fmin_powell')
    optimize(powell_chebyshev, mpipool, nodes=10, target=target)

 
# end of file
