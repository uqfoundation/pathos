#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                         June Kim & Mike McKerns, Caltech
#                        (C) 1997-2010  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
"""
pathos: a framework for heterogeneous computing

<introductory doc goes here>


Major Features
==============

<feature summary goes here>


Current Release
===============

This release version is pathos-0.1a1. You can download it here.
The latest version of pathos is available from::
    http://dev.danse.us/trac/pathos

Pathos is distributed under a modified BSD license.


Installation
============

Pathos is packaged to install from source, so you must
download the tarball, unzip, and run the installer::
    [download]
    $ tar -xvzf pathos-0.1a1.tgz
    $ cd pathos-0.1a1
    $ python setup py build
    $ python setup py install

You will be warned of any missing dependencies and/or settings after
you run the "build" step above. Pathos depends on dill...
...so you should install them first.

Alternately, pathos can be installed with easy_install::
    [download]
    $ easy_install -f . pathos


Requirements
============

Pathos requires::
    - python, version >= 2.5, version < 3.0
    - dill, version >= 0.1a1
    - pox, version >= 0.1a1
    - pyina, version >= 0.1a1
    - pyre, version == 0.8-pathos (*)
    - pp, version == 1.5.7-pathos (*)

Optional requirements::
    - setuptools, version >= 0.6
    - rpyc, version >= 3.0.6


Usage Notes
===========

<usage doc goes here>


More Information
================

Please see http://dev.danse.us/trac/pathos/pyina for further information.
"""
__version__ = '0.1a1'
__author__ = 'Mike McKerns'

__license__ = """
This software is part of the open-source DANSE project at the California
Institute of Technology, and is available subject to the conditions and
terms laid out below. By downloading and using this software you are
agreeing to the following conditions.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met::

    - Redistribution of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    - Redistribution in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentations and/or other materials provided with the distribution.

    - Neither the name of the California Institute of Technology nor
      the names of its contributors may be used to endorse or promote
      products derived from this software without specific prior written
      permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Copyright (c) 2010 California Institute of Technology. All rights reserved.


If you use this software to do productive scientific research that leads to
publication, we ask that you acknowledge use of the software by citing the
following paper in your publication::

    "pathos: a framework for heterogeneous computing",
     Michael McKerns and Michael Aivazis, unpublished;
     http://dev.danse.us/trac/pathos

"""
# high-level interface
import core
import hosts

# launchers
from LauncherSSH import LauncherSSH as SSH_Launcher
from LauncherSCP import LauncherSCP as SCP_Launcher

# tunnels
from Tunnel import Tunnel as SSH_Tunnel

# mappers
import pp_map

# strategies

# tools, utilities, etc
import util

def copyright():
    """print copyright and reference"""
    print __license__[-417:]
    return

# end of file
