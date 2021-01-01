#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2021 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE
"""
Chebyshev's polynomials
"""
from numpy import sum as numpysum
from numpy import asarray
from mystic.math import polyeval, poly1d

# coefficients for specific Chebyshev polynomials
chebyshev2coeffs = [2., 0., -1.]
chebyshev4coeffs = [8., 0., -8., 0., 1.]
chebyshev6coeffs = [32., 0., -48., 0., 18., 0., -1.]
chebyshev8coeffs = [128., 0., -256., 0., 160., 0., -32., 0., 1.]
chebyshev16coeffs = [32768., 0., -131072., 0., 212992., 0., -180224., 0., 84480., 0., -21504., 0., 2688., 0., -128., 0., 1]

def chebyshevcostfactory(target):
    def chebyshevcost(trial,M=61):
        """The costfunction for order-n Chebyshev fitting.
M evaluation points between [-1, 1], and two end points"""

        result=0.0
        x=-1.0
        dx = 2.0 / (M-1)
        for i in range(M):
            px = polyeval(trial, x)
            if px<-1 or px>1:
                result += (1 - px) * (1 - px)
            x += dx

        px = polyeval(trial, 1.2) - polyeval(target, 1.2)
        if px<0: result += px*px

        px = polyeval(trial, -1.2) - polyeval(target, -1.2)
        if px<0: result += px*px

        return result
    return chebyshevcost

# prepared cost factories
chebyshev2cost = chebyshevcostfactory(chebyshev2coeffs)
chebyshev4cost = chebyshevcostfactory(chebyshev4coeffs)
chebyshev6cost = chebyshevcostfactory(chebyshev6coeffs)
chebyshev8cost = chebyshevcostfactory(chebyshev8coeffs)
chebyshev16cost = chebyshevcostfactory(chebyshev16coeffs)


# End of file
