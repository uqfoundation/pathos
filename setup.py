#!/usr/bin/env python
#
# Michael McKerns
# mmckerns@caltech.edu

# check if easy_install is available
try:
#   import __force_distutils__ #XXX: uncomment to force use of distutills
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False

# platform-specific instructions
from sys import platform
if platform[:3] == 'win':
    pass
else: #platform = linux or mac
    if platform[:6] == 'darwin':
        pass
    pass

# build the 'setup' call
setup_code = """
setup(name="pathos",
    version="0.1a2.dev",
    maintainer="Mike McKerns",
    maintainer_email="mmckerns@caltech.edu",
    license="BSD",
    platforms=["any"],
    description="a framework for heterogeneous computing",
    classifiers=(
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Physics Programming"),

    packages=['pathos'],
    package_dir={'pathos':'pathos'},
"""

# add dependencies
pyre_version = '==0.8-pathos' # NOTE: repackaging; includes 'journal'
pp_version = '==1.5.7-pathos' # NOTE: modified redistribution
dill_version = '>=0.1a1'      # NOTE: implicit dependency
pox_version = '>=0.1a1'
pyina_version = '>=0.1a1'
rpyc_version = '>=3.0.6'
processing_version = '>=0.52'
if has_setuptools:
    setup_code += """
        zip_safe = False,
        dependency_links = ['http://dev.danse.us/packages/'],
        install_requires = ['pp%s','dill%s','pox%s','pyre%s','processing%s'], #'pyina%s'],
""" % (pp_version, dill_version, pox_version, pyre_version, processing_version, pyina_version)

# add the scripts, and close 'setup' call
setup_code += """
    scripts=['scripts/pathos_server.py',
             'scripts/pathos_tunnel.py',
             'scripts/tunneled_pathos_server.py',
             'pathos/portpicker.py'])
"""

# exec the 'setup' code
exec setup_code

# if dependencies are missing, print a warning
try:
    import pyre
    import pp
    if pp.__version__ != pp_version[2:]:
        raise ImportError
    import dill
    import pox
   #import pyina
    try:
        import multiprocessing
    except ImportError:
        import processing
except ImportError:
    print "\n***********************************************************"
    print "WARNING: One of the following dependencies is unresolved:"
    print "    pp %s" % pp_version
    print "    pyre %s" % pyre_version
    print "    dill %s" % dill_version
    print "    pox %s" % pox_version
    print "    processing %s" % processing_version
    print "    pyina %s" % pyina_version
    print "***********************************************************\n"

    print """
Pathos relies on modified distributions of '%s' and '%s'.
Please download and install unresolved dependencies here:
  http://dev.danse.us/packages/
or from the "external" directory included in the pathos source distribution.
""" % ('pp','pyre')


if __name__=='__main__':
    pass

# End of file
