#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
"""
establish a tunnel to first available remote port using pathos.util.portnumber

Usage: python pathos_tunnel.py [hostname] 
    [hostname] - name of the host with which to establish a ssh tunnel
"""

from pathos.core import *

if __name__ == '__main__':

##### CONFIGURATION & INPUT ########################
  # set the default remote host
  rhost = 'localhost'
 #rhost = 'foobar.danse.us'
 #rhost = 'computer.cacr.caltech.edu'

  print("""Usage: python pathos_tunnel.py [hostname] 
    [hostname] - name of the host with which to establish a ssh tunnel,
    if omitted, tries "%s".""" % rhost)

  # get remote hostname from user
  import sys
  if '--help' in sys.argv:
    sys.exit(0)
  try:
    myhost = sys.argv[1]
  except: myhost = None
  if myhost:
    rhost = myhost #XXX: should test rhost validity here...
  else: pass # use default
##### CONFIGURATION & INPUT ########################

  # establish ssh tunnel
  tunnel = connect(rhost)
  print('executing {ssh -N -L %d:%s:%d}' % (tunnel._lport,rhost,tunnel._rport))

  # do stuff (i.e. wait) while the tunnel is connected
  import sys
  print('Press <Enter> to disconnect')
  sys.stdin.readline()

  # disconnect tunnel
  tunnel.disconnect()
  # FIXME: just kills 'ssh', not the tunnel
  # get local pid: ps u | grep "ssh -N -L%s:%s$s" % (lport,rhost,rport)
  # kill -15 int(tunnelpid)


# EOF
