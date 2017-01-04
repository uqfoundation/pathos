#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE

def fmin_powell(cost, x0, full=1, disp=1, monitor=0):
    """ change default behavior for selected optimizers """
    from mystic.solvers import fmin_powell as solver
    from mystic.monitors import Monitor, VerboseMonitor
    if monitor: mon = VerboseMonitor(10)
    else: mon = Monitor()
    npop = 10*len(x0)
    solved = solver(cost, x0, npop=npop, full_output=full,
                                         disp=disp, itermon=mon, handler=0)
    # return: solution, energy, generations, fevals
    return solved[0], solved[1], solved[2], solved[3]

def diffev(cost, x0, full=1, disp=1, monitor=0):
    """ change default behavior for selected optimizers """
    from mystic.solvers import diffev as solver
    from mystic.monitors import Monitor, VerboseMonitor
    if monitor: mon = VerboseMonitor(10)
    else: mon = Monitor()
    npop = 10*len(x0)
    solved = solver(cost, x0, npop=npop, full_output=full,
                                         disp=disp, itermon=mon, handler=0)
    # return: solution, energy, generations, fevals
    return solved[0], solved[1], solved[2], solved[3]


def best_results(results):
    """ get the results with the lowest energy """
    results = list(results) # in case we used an iterator
    best = list(results[0][0]), results[0][1]
    bestpath = results[0][2]
    besteval = results[0][3]
    func_evals = besteval
    for result in results[1:]:
      func_evals += result[3]  # add function evaluations
      if result[1] < best[1]: # compare energy
        best = list(result[0]), result[1]
        bestpath = result[2]
        besteval = result[3]
    # return best: solution, energy, generations, fevals
    return best[0], best[1], bestpath, besteval, func_evals


# EOF
