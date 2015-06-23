#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2008-2015 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
#
# backward compatibility
__all__ = ['ParallelPythonPool', 'stats']
from pathos.parallel import __doc__
from pathos.parallel import cpu_count, ParallelPool as ParallelPythonPool
from pathos.parallel import __print_stats, stats

# EOF
