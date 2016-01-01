#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2008-2016 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
#
# backward compatibility
__all__ = ['PythonSerial']
from pathos.serial import __doc__, __STATE
from pathos.serial import *
PythonSerial = SerialPool

# EOF
