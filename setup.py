#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2021 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE

import os
import sys
# drop support for older python
unsupported = None
if sys.version_info < (2, 7):
    unsupported = 'Versions of Python before 2.7 are not supported'
elif (3, 0) <= sys.version_info < (3, 6):
    unsupported = 'Versions of Python before 3.6 are not supported'
if unsupported:
    raise ValueError(unsupported)

# set version numbers
stable_version = '0.2.8'
target_version = '0.2.8'
is_release = stable_version == target_version

# check if easy_install is available
try:
#   import __force_distutils__ #XXX: uncomment to force use of distutills
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False

# generate version number
if os.path.exists('pathos/info.py'):
    # is a source distribution, so use existing version
    os.chdir('pathos')
    with open('info.py','r') as f:
        f.readline() # header
        this_version = f.readline().split()[-1].strip("'")
    os.chdir('..')
elif stable_version == target_version:
    # we are building a stable release
    this_version = target_version
else:
    # we are building a distribution
    this_version = target_version + '.dev0'
    if is_release:
      from datetime import date
      today = "".join(date.isoformat(date.today()).split('-'))
      this_version += "-" + today

# get the license info
with open('LICENSE') as file:
    license_text = file.read()

# generate the readme text
long_description = \
"""--------------------------------------------------------------------------
pathos: parallel graph management and execution in heterogeneous computing
--------------------------------------------------------------------------

About the Pathos Framework
==========================

``pathos`` is a framework for heterogeneous computing. It provides a consistent
high-level interface for configuring and launching parallel computations
across heterogeneous resources. ``pathos`` provides configurable launchers for
parallel and distributed computing, where each launcher contains the
syntactic logic to configure and launch jobs in an execution environment.
Examples of launchers that plug into ``pathos`` are: a queue-less MPI-based
launcher (in ``pyina``), a ssh-based launcher (in ``pathos``), and a multi-process
launcher (in ``multiprocess``).

``pathos`` provides a consistent interface for parallel and/or distributed
versions of ``map`` and ``apply`` for each launcher, thus lowering the barrier
for users to extend their code to parallel and/or distributed resources.
The guiding design principle behind ``pathos`` is that ``map`` and ``apply``
should be drop-in replacements in otherwise serial code, and thus switching
to one or more of the ``pathos`` launchers is all that is needed to enable
code to leverage the selected parallel or distributed computing resource.
This not only greatly reduces the time to convert a code to parallel, but it
also enables a single code-base to be maintained instead of requiring
parallel, serial, and distributed versions of a code. ``pathos`` maps can be
nested, thus hierarchical heterogeneous computing is possible by merely
selecting the desired hierarchy of ``map`` and ``pipe`` (``apply``) objects.

The ``pathos`` framework is composed of several interoperating packages:

    - ``dill``: a utility to serialize all of python
    - ``pox``: utilities for filesystem exploration and automated builds
    - ``klepto``: persistent caching to memory, disk, or database
    - ``multiprocess``: better multiprocessing and multithreading in python
    - ``ppft``: distributed and parallel python
    - ``pyina``: MPI parallel ``map`` and cluster scheduling
    - ``pathos``: graph management and execution in heterogeneous computing


About Pathos
============

The ``pathos`` package provides a few basic tools to make parallel and
distributed computing more accessible to the end user. The goal of ``pathos``
is to enable the user to extend their own code to parallel and distributed
computing with minimal refactoring.

``pathos`` provides methods for configuring, launching, monitoring, and
controlling a service on a remote host. One of the most basic features
of ``pathos`` is the ability to configure and launch a RPC-based service
on a remote host. ``pathos`` seeds the remote host with the  ``portpicker``
script, which allows the remote host to inform the localhost of a port
that is available for communication.

Beyond the ability to establish a RPC service, and then post requests,
is the ability to launch code in parallel. Unlike parallel computing
performed at the node level (typically with MPI), ``pathos`` enables the
user to launch jobs in parallel across heterogeneous distributed resources.
``pathos`` provides distributed ``map`` and ``pipe`` algorithms, where a mix of
local processors and distributed workers can be selected.  ``pathos``
also provides a very basic automated load balancing service, as well as
the ability for the user to directly select the resources.

The high-level ``pool.map`` interface, yields a ``map`` implementation that
hides the RPC internals from the user. With ``pool.map``, the user can launch
their code in parallel, and as a distributed service, using standard python
and without writing a line of server or parallel batch code.

RPC servers and communication in general is known to be insecure.  However,
instead of attempting to make the RPC communication itself secure, ``pathos``
provides the ability to automatically wrap any distributes service or
communication in a ssh-tunnel. Ssh is a universally trusted method.
Using ssh-tunnels, ``pathos`` has launched several distributed calculations
on national lab clusters, and to date has performed test calculations
that utilize node-to-node communication between several national lab clusters
and a user's laptop.  ``pathos`` allows the user to configure and launch
at a very atomistic level, through raw access to ssh and scp. 

``pathos`` is the core of a python framework for heterogeneous computing.
``pathos`` is in active development, so any user feedback, bug reports, comments,
or suggestions are highly appreciated.  A list of issues is located at https://github.com/uqfoundation/pathos/issues, with a legacy list maintained at https://uqfoundation.github.io/project/pathos/query.


Major Features
==============

``pathos`` provides a configurable distributed parallel ``map`` interface
to launching RPC service calls, with:

    - a ``map`` interface that meets and extends the python ``map`` standard
    - the ability to submit service requests to a selection of servers
    - the ability to tunnel server communications with ssh

The ``pathos`` core is built on low-level communication to remote hosts using
ssh. The interface to ssh, scp, and ssh-tunneled connections can:

    - configure and launch remote processes with ssh
    - configure and copy file objects with scp
    - establish an tear-down a ssh-tunnel

To get up and running quickly, ``pathos`` also provides infrastructure to:

    - easily establish a ssh-tunneled connection to a RPC server


Current Release
===============

This documentation is for version ``pathos-%(thisver)s``.

The latest released version of ``pathos`` is available from:

    https://pypi.org/project/pathos

``pathos`` is distributed under a 3-clause BSD license.

    >>> import pathos
    >>> pathos.license()


Development Version
===================

You can get the latest development version with all the shiny new features at:

    https://github.com/uqfoundation

If you have a new contribution, please submit a pull request.


Installation
============

``pathos`` is packaged to install from source, so you must
download the tarball, unzip, and run the installer::

    [download]
    $ tar -xvzf pathos-%(relver)s.tar.gz
    $ cd pathos-%(relver)s
    $ python setup py build
    $ python setup py install

You will be warned of any missing dependencies and/or settings
after you run the "build" step above.  ``pathos`` depends on ``dill`` and
``pox``, each of which are essentially subpackages of ``pathos`` but are
released independently. ``pathos`` also depends on ``multiprocess`` and
``ppft``.  You must install all of the ``pathos`` framework packages for
``pathos`` to provide the full functionality for heterogeneous computing. 

Alternately, ``pathos`` can be installed with ``pip`` or ``easy_install``::

    $ pip install pathos


Requirements
============

``pathos`` requires:

    - ``python``, **version == 2.7** or **version >= 3.6**, or ``pypy``
    - ``dill``, **version >= 0.3.4**
    - ``pox``, **version >= 0.3.0**
    - ``ppft``, **version >= 1.6.6.4**
    - ``multiprocess``, **version >= 0.70.12**

Optional requirements:

    - ``setuptools``, **version >= 0.6**
    - ``pyina``, **version >= 0.2.4**
    - ``rpyc``, **version >= 3.0.6**
    - ``mystic``, **version >= 0.3.7**


More Information
================

Probably the best way to get started is to look at the documentation at
http://pathos.rtfd.io. Also see ``pathos.tests`` and ``pathos.examples``
for a set of scripts that demonstrate the configuration and launching of
communications with ssh and scp, and demonstrate the configuration and
execution of jobs in a hierarchical parallel workflow. You can run the test
suite with ``python -m pathos.tests``. Tunnels and other connections to
remote servers can be established with the ``pathos_connect`` script (or with
``python -m pathos``). See ``pathos_connect --help`` for more information.
``pathos`` also provides a ``portpicker`` script to select an open port
(also available with ``python -m pathos.portpicker``). The source code is 
generally well documented, so further questions may be resolved by inspecting
the code itself.  Please feel free to submit a ticket on github, or ask a
question on stackoverflow (**@Mike McKerns**).
If you would like to share how you use ``pathos`` in your work, please send
an email (to **mmckerns at uqfoundation dot org**).

Important classes and functions are found here:

    - ``pathos.abstract_launcher``           [the worker pool API definition]
    - ``pathos.pools``                       [all of the pathos worker pools]
    - ``pathos.core``                        [the high-level command interface] 
    - ``pathos.hosts``                       [the hostname registry interface] 
    - ``pathos.serial.SerialPool``           [the serial python worker pool]
    - ``pathos.parallel.ParallelPool``       [the parallelpython worker pool]
    - ``pathos.multiprocessing.ProcessPool`` [the multiprocessing worker pool]
    - ``pathos.threading.ThreadPool``        [the multithreading worker pool]
    - ``pathos.connection.Pipe``             [the launcher base class]
    - ``pathos.secure.Pipe``                 [the secure launcher base class]
    - ``pathos.secure.Copier``               [the secure copier  base class]
    - ``pathos.secure.Tunnel``               [the secure tunnel base class]
    - ``pathos.selector.Selector``           [the selector base class]
    - ``pathos.server.Server``               [the server base class]
    - ``pathos.profile``                     [profiling in threads and processes]

``pathos`` also provides two convenience scripts that are used to establish
secure distributed connections. These scripts are installed to a directory
on the user's ``$PATH``, and thus can be run from anywhere:

    - ``portpicker``                         [get the portnumber of an open port]
    - ``pathos_connect``                     [establish tunnel and/or RPC server]

Typing ``--help`` as an argument to any of the above scripts will print out an
instructive help message.


Citation
========

If you use ``pathos`` to do research that leads to publication, we ask that you
acknowledge use of ``pathos`` by citing the following in your publication::

    M.M. McKerns, L. Strand, T. Sullivan, A. Fang, M.A.G. Aivazis,
    "Building a framework for predictive science", Proceedings of
    the 10th Python in Science Conference, 2011;
    http://arxiv.org/pdf/1202.1056

    Michael McKerns and Michael Aivazis,
    "pathos: a framework for heterogeneous computing", 2010- ;
    https://uqfoundation.github.io/project/pathos

Please see https://uqfoundation.github.io/project/pathos or
http://arxiv.org/pdf/1202.1056 for further information.

""" % {'relver' : stable_version, 'thisver' : this_version}

# write readme file
with open('README', 'w') as file:
    file.write(long_description)

# generate 'info' file contents
def write_info_py(filename='pathos/info.py'):
    contents = """# THIS FILE GENERATED FROM SETUP.PY
this_version = '%(this_version)s'
stable_version = '%(stable_version)s'
readme = '''%(long_description)s'''
license = '''%(license_text)s'''
"""
    with open(filename, 'w') as file:
        file.write(contents % {'this_version' : this_version,
                               'stable_version' : stable_version,
                               'long_description' : long_description,
                               'license_text' : license_text })
    return

# write info file
write_info_py()

# platform-specific instructions
from sys import platform, version_info
if platform[:3] == 'win':
    pass
else: #platform = linux or mac
    if platform[:6] == 'darwin':
        pass
    pass

# build the 'setup' call
setup_code = """
setup(name="pathos",
    version='%s',
    description="parallel graph management and execution in heterogeneous computing",
    long_description = '''%s''',
    author = 'Mike McKerns',
    maintainer = 'Mike McKerns',
    license = '3-clause BSD',
    platforms = ['Linux', 'Windows', 'Mac'],
    url = 'https://github.com/uqfoundation/pathos',
    download_url = 'https://github.com/uqfoundation/pathos/releases/download/pathos-%s/pathos-%s.tar.gz',
    classifiers = ['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: BSD License',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Software Development'],

    packages=['pathos','pathos.tests',\
              'pathos.helpers','pathos.secure','pathos.xmlrpc'],
    package_dir={'pathos':'pathos', 'pathos.tests':'tests', \
                 'pathos.helpers':'pathos/helpers', \
                 'pathos.secure':'pathos/secure', \
                 'pathos.xmlrpc':'pathos/xmlrpc', \
                },
""" % (target_version, long_description, stable_version, stable_version)

'''
# check for 'processing'
try: #NOTE: odd... if processing is installed, *don't* install multiprocess
    from processing import __version__ as processing_version
    if processing_version >= '0.52-pathos': # NOTE: modified redistribution
        processing_version = '=='+processing_version
        mp_version = ''
    else: raise AttributeError('multiprocess')
except Exception:
    mp_version = '>=0.70.12' # 0.70a1 py25-py33, 0.52 on py25, None on py34
    processing_version = ''
'''

# add dependencies
ppft_version = '>=1.6.6.4'
dill_version = '>=0.3.4'
pox_version = '>=0.3.0'
mp_version = '>=0.70.12' if version_info >= (2,6) else '>=0.52.0'
pyina_version = '>=0.2.4'
rpyc_version = '>=3.0.6'
deps = [ppft_version, dill_version, pox_version]
if mp_version:
    deps = tuple(deps + ["'multiprocess%s']," % mp_version])
else:
    deps = tuple(deps + ["],"])
if has_setuptools:
    setup_code += """
        zip_safe = False,
        install_requires = ['ppft%s','dill%s','pox%s',%s
""" % deps

# add the scripts, and close 'setup' call
setup_code += """
    scripts=['scripts/pathos_connect',
             'scripts/portpicker'])
"""

# exec the 'setup' code
exec(setup_code)

# if dependencies are missing, print a warning
try:
    import ppft
    import dill
    import pox
    if version_info >= (2,6):
        import multiprocess
    else:
        import processing
   #try:
   #    import processing
   #except ImportError:
   #    import multiprocess
   #    if getattr(multiprocess, '__version__', '0.70a1') == '0.70a1':
   #        raise ImportError
except ImportError:
    print("\n***********************************************************")
    print("WARNING: One of the following dependencies is unresolved:")
    print("    ppft %s" % ppft_version)
    print("    dill %s" % dill_version)
    print("    pox %s" % pox_version)
    print("    multiprocess %s" % mp_version)
    print("***********************************************************\n")

#    print("""
#If '%s' is installed, '%s' will be regarded as optional, and thus will
#not be installed.  Note that '%s' is not available through a standard
#install, however it may be downloaded from:
#  http://dev.danse.us/packages/
#or found in the "external" directory included in the pathos source distribution
#""" % ('processing','multiprocess','processing'))


if __name__=='__main__':
    pass

# End of file
