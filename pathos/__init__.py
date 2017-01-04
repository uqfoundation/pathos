#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Author: June Kim (jkim @caltech)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE

from __future__ import absolute_import

# get version numbers, license, and long description
try:
    from .info import this_version as __version__
    from .info import readme as __doc__, license as __license__
except ImportError:
    msg = """First run 'python setup.py build' to build pathos."""
    raise ImportError(msg)

__author__ = 'Mike McKerns'

__doc__ = """
""" + __doc__

__license__ = """
""" + __license__

# logger
def logger(level=None, handler=None, **kwds):
    import logging
    name = kwds.get('name', 'pathos')
    log = logging.getLogger(name)
    if handler is not None:
        log.handlers = []
        log.addHandler(handler)
    elif not len(log.handlers):
        log.addHandler(logging.StreamHandler())
    if level is not None:
        log.setLevel(level)
    return log

# high-level interface
from . import core
from . import hosts
from . import server
from . import selector
from . import connection
from . import pools

# worker pools
from . import serial
from . import parallel
from . import multiprocessing
from . import threading

# tools, utilities, etc
from . import util

# backward compatibility
python = serial
pp = parallel
from pathos.secure import Pipe as SSH_Launcher
from pathos.secure import Copier as SCP_Launcher
from pathos.secure import Tunnel as SSH_Tunnel


def license():
    """print license"""
    print(__license__)
    return

def citation():
    """print citation"""
    print(__doc__[-501:-123])
    return

# end of file
