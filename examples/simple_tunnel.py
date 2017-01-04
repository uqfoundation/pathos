#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
"""
example of building a simple ssh-tunnel

To run: python simple_tunnel.py
"""

from pathos.secure import Tunnel

if __name__ == '__main__':
    import sys
    rhost = 'localhost'
   #rhost = 'foobar.danse.us'
   #rhost = 'computer.cacr.caltech.edu'
    rport = 23

    t = Tunnel('Tunnel')
    lport = t.connect(rhost, rport)
    print('SSH Tunnel to: %s' % rhost)
    print('Remote port: %s' % rport)
    print('Local port: %s' % lport)
    print('Press <Enter> to disconnect')
    sys.stdin.readline()
    t.disconnect()
