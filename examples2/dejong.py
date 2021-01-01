#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2021 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE
"""
Rosenbrock's function
"""

from numpy import sum as numpysum
from numpy import asarray

def rosen(coeffs):
    """evaluates n-dimensional Rosenbrock function for a list of coeffs
minimum is f(x)=0.0 at xi=1.0"""
    x = [1]*2 # ensure that there are 2 coefficients
    x[:len(coeffs)]=coeffs
    x = asarray(x) #XXX: must be a numpy.array
    return numpysum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)#,axis=0)


# End of file
