#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE
"""
Minimize the selected model with Powell's method.

Requires: development version of mystic
  http://pypi.python.org/pypi/mystic
"""

def optimize(solver, target='rosen', **kwds):
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
    print("One trial:")
    print("===============")

    # initial guess
    import random
    x0 = [random.uniform(-100,100) for i in range(ndim)]

    # minimize the function
    results = the_solver(the_model, x0, **kwds)

    print("===============")
    print("Actual params:\n %s" % pprint(actual_coeffs))
    print("Solved params:\n %s" % pprint(results[0]))
    print("Function value: %s" % results[1])
    print("Total function evals: %s" % results[3])
    return 

# Powell's Directonal solver
from optimize_helper import fmin_powell as the_solver


if __name__ == '__main__':
    target = 'rosen'
   #target = 'cheby'
    print("Function: %s" % target)
    print("Solver: %s" % 'fmin_powell')
    optimize(the_solver, target=target)
   #optimize(the_solver, target=target, monitor=True)
   #optimize(the_solver, target=target, monitor=True, disp=False)

 
# end of file
