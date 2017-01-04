#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
"""
pools: pools of pathos workers, providing map and pipe constructs
"""

from pathos.helpers import ProcessPool as _ProcessPool
from pathos.helpers import ThreadPool as _ThreadPool
from pathos.multiprocessing import ProcessPool
from pathos.threading import ThreadPool
from pathos.parallel import ParallelPool
from pathos.serial import SerialPool
