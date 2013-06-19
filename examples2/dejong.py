#!/usr/bin/env python
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
