#!/usr/bin/env python
"""
start tunneled remote server for selected package
"""

from pathos.core import *
from pathos.hosts import get_profile, register_profiles


if __name__ == '__main__':

##### CONFIGURATION & INPUT ########################
  # set the default remote host
 #rhost = 'localhost'
  rhost = 'upgrayedd.danse.us'
 #rhost = 'shc-b.cacr.caltech.edu'
 #rhost = 'login.cacr.caltech.edu'

  # set the default server command
  server = 'ppserver'  #XXX: "ppserver -p %s" % rport
 #server = 'classic_server'  #XXX: "classic_server -p %s" % rport
 #server = 'registry_server'  #XXX: "registry_server -p %s" % rport

  print """Usage: python start_server.py [hostname] [server] 
    [hostname] - name of the host on which to run the server
    [server] - name of the RPC server (assumed to be already installed)
    defaults are: "%s" "%s".""" % (rhost, server)

  # get remote hostname from user
  import sys
  try:
    myinp = sys.argv[1]
  except: myinp = None
  if myinp:
    rhost = myinp #XXX: should test rhost validity here... (how ?)
  else: pass # use default
  del myinp

  # my remote environment (should be auto-detected)
  profiles = {'upgrayedd.danse.us':'.profile',
              'login.cacr.caltech.edu':'.cshrc'}
  register_profiles(profiles)
  profile = get_profile(rhost)

  # get server to run from user
  import sys
  try:
    myinp = sys.argv[2]
  except: myinp = None
  if myinp:
    server = myinp #XXX: should test validity here... (filename)
  else: pass # use default
  del myinp
##### CONFIGURATION & INPUT ########################

  # get available remote port number
  rport = pickport(rhost)

  # establish ssh tunnel
  tunnel,lport = connect(rhost,rport)
  print 'executing {ssh -N -L %d:%s:%d}' % (lport,rhost,rport)

  # run server
  serve(server,rhost,rport, profile=profile)

  # get server pid  #FIXME: launcher.pid is not pid(server)
  target = 'python[^#]*'+server #XXX: filter w/ regex for python-based server
  pid = getpid(target,rhost)

  # test server
  # XXX: add a simple one-liner...
  print "\nServer running at port=%s with pid=%s" % (rport,pid)
  print "Connected to localhost at port=%s" % (lport)
  import sys
  print 'Press <Enter> to kill server'
  sys.stdin.readline()

  # stop server
  print kill(pid,rhost)
# del rserver  #XXX: delete should run self.kill (?)

  # disconnect tunnel
  tunnel.disconnect()
  # FIXME: just kills 'ssh', not the tunnel
  # get local pid: ps u | grep "ssh -N -L%s:%s$s" % (lport,rhost,rport)
  # kill -15 int(tunnelpid)


# EOF
