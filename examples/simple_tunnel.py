#!/usr/bin/env python
"""
example of building a simple ssh-tunnel

To run: python simple_tunnel.py
"""

from pathos import SSH_Tunnel


if __name__ == '__main__':
    import sys
    rhost = 'localhost'
   #rhost = 'foobar.danse.us'
   #rhost = 'computer.cacr.caltech.edu'
    rport = 23

    t = SSH_Tunnel('Tunnel')
    lport = t.connect(rhost, rport)
    print 'SSH Tunnel to:', rhost
    print 'Remote port:', rport
    print 'Local port:', lport
    print 'Press <Enter> to disconnect'
    sys.stdin.readline()
    t.disconnect()
