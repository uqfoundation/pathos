#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Author: June Kim (jkim @caltech)
# Copyright (c) 1997-2015 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE

# get version numbers, license, and long description
try:
    from info import this_version as __version__
    from info import readme as __doc__, license as __license__
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
import core
import hosts

# launchers
from LauncherSSH import LauncherSSH as SSH_Launcher
from LauncherSCP import LauncherSCP as SCP_Launcher

# tunnels
from Tunnel import Tunnel as SSH_Tunnel

# worker pools
import pools
import serial
import parallel
import multiprocessing
import threading
# backward compatibility
python = serial
pp = parallel

# tools, utilities, etc
import util

def license():
    """print license"""
    print __license__
    return

def citation():
    """print citation"""
    print __doc__[-499:-140]
    return

# end of file
