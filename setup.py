#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE

import os
import sys
# drop support for older python
if sys.version_info < (3, 7):
    unsupported = 'Versions of Python before 3.7 are not supported'
    raise ValueError(unsupported)

# get distribution meta info
here = os.path.abspath(os.path.dirname(__file__))
sys.path.append(here)
from version import (__version__, __author__, __contact__ as AUTHOR_EMAIL,
                     get_license_text, get_readme_as_rst, write_info_file)
LICENSE = get_license_text(os.path.join(here, 'LICENSE'))
README = get_readme_as_rst(os.path.join(here, 'README.md'))

# write meta info file
write_info_file(here, 'pathos', doc=README, license=LICENSE,
                version=__version__, author=__author__)
del here, get_license_text, get_readme_as_rst, write_info_file

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
    version=__version__,
    description="parallel graph management and execution in heterogeneous computing",
    long_description = README.strip(),
    author = __author__,
    author_email = AUTHOR_EMAIL,
    maintainer = __author__,
    maintainer_email = AUTHOR_EMAIL,
    license = 'BSD-3-Clause',
    platforms = ['Linux', 'Windows', 'Mac'],
    url = 'https://github.com/uqfoundation/pathos',
    download_url = 'https://pypi.org/project/pathos/#files',
    project_urls = {
        'Documentation':'http://pathos.rtfd.io',
        'Source Code':'https://github.com/uqfoundation/pathos',
        'Bug Tracker':'https://github.com/uqfoundation/pathos/issues',
    },
    python_requires = '>=3.7',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
    ],
    packages=['pathos','pathos.tests',\
              'pathos.helpers','pathos.secure','pathos.xmlrpc'],
    package_dir={'pathos':'pathos', 'pathos.tests':'pathos/tests', \
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
ppft_version = 'ppft>=1.7.6.7'
dill_version = 'dill>=0.3.7'
pox_version = 'pox>=0.3.3'
mp_version = 'multiprocess>=0.70.15'
pyina_version = 'pyina>=0.2.7'
mystic_version = 'mystic>=0.4.0'
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
