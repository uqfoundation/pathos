#!/usr/bin/env python
 
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Author: June Kim (jkim @caltech)
# Copyright (c) 1997-2014 Caltech
# License: 3-clause BSD

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

# high-level interface
import core
import hosts

# launchers
from LauncherSSH import LauncherSSH as SSH_Launcher
from LauncherSCP import LauncherSCP as SCP_Launcher

# tunnels
from Tunnel import Tunnel as SSH_Tunnel

# worker pools
import python
import multiprocessing
import pp

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
