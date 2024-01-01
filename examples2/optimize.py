#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2024 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE
"""
Minimize the selected model with Powell's method.

Requires: development version of mystic
  http://pypi.python.org/pypi/mystic
"""

def optimize(solver, nodes, target='rosen', **kwds):
    if target == 'rosen': # 3d-rosenbrock
        # Rosenbrock function
        from dejong import rosen as the_model
        ndim = 3
        actual_coeffs = [1.0] * ndim
        pprint = list
    else: # 4th-order chebyshev
        # Chebyshev cost function
        from poly import chebyshev4cost as the_model
        from poly import chebyshev4coeffs as actual_coeffs
        ndim = len(actual_coeffs)
        from mystic.math import poly1d as pprint

    # number of trials
    N = nodes
    print("Number of trials: %s" % N)
    print("===============")

    # initial guess
    import random
    x0 = ([random.uniform(-100,100) for i in range(ndim)] for i in range(N))
    model = (the_model for i in range(N))

    # minimize the function
    results = map(the_solver, model, x0)

    # find the results with the lowest energy
    from optimize_helper import best_results
    solution = best_results(results)

    print("===============")
    print("Actual params:\n %s" % pprint(actual_coeffs))
    print("Solved params:\n %s" % pprint(solution[0]))
    print("Function value: %s" % solution[1])
    print("Total function evals: %s" % solution[4])
    return 

# Powell's Directonal solver
from optimize_helper import fmin_powell as the_solver


if __name__ == '__main__':
    target = 'rosen'
   #target = 'cheby'
    print("Function: %s" % target)
    print("Solver: %s" % 'fmin_powell')
    optimize(the_solver, nodes=3, target=target)

 
# end of file
