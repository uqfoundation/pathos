#!/usr/bin/env python
"""
get first available remote port using pathos.util.portnumber
"""

from pathos.core import *


if __name__ == '__main__':

##### CONFIGURATION & INPUT ########################
  # set the default remote host
  rhost = 'localhost'
 #rhost = 'foobar.danse.us'
 #rhost = 'computer.cacr.caltech.edu'

  print """Usage: python generate_tunnel.py [hostname] 
    [hostname] - name of the host with which to establish a ssh tunnel,
    if omitted, tries "%s".""" % rhost

  # get remote hostname from user
  import sys
  try:
    myhost = sys.argv[1]
  except: myhost = None
  if myhost:
    rhost = myhost #XXX: should test rhost validity here...
  else: pass # use default
##### CONFIGURATION & INPUT ########################

  # get available remote port number
  rport = pickport(rhost)

  # establish ssh tunnel
  tunnel,lport = connect(rhost,rport)
  print 'executing {ssh -N -L %d:%s:%d}' % (lport,rhost,rport)

  # do stuff (i.e. wait) while the tunnel is connected
  import sys
  print 'Press <Enter> to disconnect'
  sys.stdin.readline()

  # disconnect tunnel
  tunnel.disconnect()
  # FIXME: just kills 'ssh', not the tunnel
  # get local pid: ps u | grep "ssh -N -L%s:%s$s" % (lport,rhost,rport)
  # kill -15 int(tunnelpid)


# EOF
