#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2008-2016 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
#
# backward compatibility
__all__ = ['ParallelPythonPool', 'stats']
from pathos.parallel import __doc__, __print_stats, __STATE
from pathos.parallel import *
ParallelPythonPool = ParallelPool

# EOF
