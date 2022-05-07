#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2022 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE

import os
import sys
# drop support for older python
unsupported = None
if sys.version_info < (2, 7):
    unsupported = 'Versions of Python before 2.7 are not supported'
elif (3, 0) <= sys.version_info < (3, 7):
    unsupported = 'Versions of Python before 3.7 are not supported'
if unsupported:
    raise ValueError(unsupported)

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

# This is a hack to import a minimal package for the build process
builtins.__PATHOS_SETUP__ = True
sys.path.append(os.path.abspath(os.path.curdir))
import pathos

# get version numbers, long_description, etc
AUTHOR = pathos.__author__
VERSION = pathos.__version__
LONG_DOC = pathos.__doc__ #FIXME: near-duplicate of README.md
#LICENSE = pathos.__license__ #FIXME: duplicate of LICENSE
AUTHOR_EMAIL = 'mmckerns@uqfoundation.org'

# check if setuptools is available
try:
    from setuptools import setup
    from setuptools.dist import Distribution
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    Distribution = object
    has_setuptools = False

# build the 'setup' call
setup_kwds = dict(
    name="pathos",
    version=VERSION,
    description="parallel graph management and execution in heterogeneous computing",
    long_description = LONG_DOC,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    maintainer = AUTHOR,
    maintainer_email = AUTHOR_EMAIL,
    license = '3-clause BSD',
    platforms = ['Linux', 'Windows', 'Mac'],
    url = 'https://github.com/uqfoundation/pathos',
    download_url = 'https://pypi.org/project/pathos/#files',
    python_requires = '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
    classifiers = ['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: BSD License',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9',
                   'Programming Language :: Python :: 3.10',
                   'Programming Language :: Python :: Implementation :: PyPy',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Software Development'],
    packages=['pathos','pathos.tests',\
              'pathos.helpers','pathos.secure','pathos.xmlrpc'],
    package_dir={'pathos':'pathos', 'pathos.tests':'tests', \
                 'pathos.helpers':'pathos/helpers', \
                 'pathos.secure':'pathos/secure', \
                 'pathos.xmlrpc':'pathos/xmlrpc', \
                },
    scripts=['scripts/pathos_connect', 'scripts/portpicker'],
)

# force python-, abi-, and platform-specific naming of bdist_wheel
class BinaryDistribution(Distribution):
    """Distribution which forces a binary package with platform name"""
    def has_ext_modules(foo):
        return True

# define dependencies
ppft_version = 'ppft>=1.6.6.4'
dill_version = 'dill>=0.3.4'
pox_version = 'pox>=0.3.0'
mp_version = 'multiprocess>=0.70.12.1'
pyina_version = 'pyina>=0.2.5'
mystic_version = 'mystic>=0.3.8'
# add dependencies
depend = [ppft_version, dill_version, pox_version, mp_version]
extras = {'examples': [mystic_version, pyina_version]}
# update setup kwds
if has_setuptools:
    setup_kwds.update(
        zip_safe=False,
        # distclass=BinaryDistribution,
        install_requires=depend,
        # extras_require=extras,
    )

# call setup
setup(**setup_kwds)

# if dependencies are missing, print a warning
try:
    import ppft
    import dill
    import pox
    import multiprocess
    #import mystic
    #import pyina
except ImportError:
    print("\n***********************************************************")
    print("WARNING: One of the following dependencies is unresolved:")
    print("    %s" % ppft_version)
    print("    %s" % dill_version)
    print("    %s" % pox_version)
    print("    %s" % mp_version)
    #print("    %s (optional)" % mystic_version)
    #print("    %s (optional)" % pyina_version)
    print("***********************************************************\n")


if __name__=='__main__':
    pass

# end of file
