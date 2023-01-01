#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE
"""
demonstrate pathos's spawn2 function
"""

from pathos.util import spawn2, _b, _str


if __name__ == '__main__':

    import os
    
    def onParent(pid, fromchild, tochild):
        s = _str(fromchild.readline())
        print(s, end='')
        tochild.write(_b('hello son\n'))
        tochild.flush()
        os.wait()

    def onChild(pid, fromparent, toparent):
        toparent.write(_b('hello dad\n'))
        toparent.flush()
        s = _str(fromparent.readline())
        print(s, end='')
        os._exit(0)

    spawn2(onParent, onChild)

    
# End of file
