#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
"""
start remote server for selected package

Usage: python pathos_server.py [hostname] [server] [remoteport] 
    [hostname] - name of the host on which to run the server
    [server] - name of the RPC server (assumed to be already installed)
    [remoteport] - remote port over which the server will communicate
"""

from pathos.core import *
from pathos.hosts import get_profile, register_profiles


if __name__ == '__main__':
  ### ASSUME ALL PACKAGES ARE INSTALLED ###

##### CONFIGURATION & INPUT ########################
  # set the default remote host
  rhost = 'localhost'
 #rhost = 'foobar.danse.us'
 #rhost = 'computer.cacr.caltech.edu'

  # set any 'special' profiles (those which don't use default_profie)
  profiles = {'foobar.danse.us':'.profile',
              'computer.cacr.caltech.edu':'.cshrc'}

  # set the default port
  rport = '98909'
  # set the default server command
  server = 'ppserver'  #XXX: "ppserver -p %s" % rport
 #server = 'classic_server'  #XXX: "classic_server -p %s" % rport
 #server = 'registry_server'  #XXX: "registry_server -p %s" % rport

  print("""Usage: python pathos_server.py [hostname] [server] [remoteport] 
    [hostname] - name of the host on which to run the server
    [server] - name of the RPC server (assumed to be already installed)
    [remoteport] - remote port over which the server will communicate
    defaults are: "%s" "%s" "%s".""" % (rhost, server, rport))

  # get remote hostname from user
  import sys
  if '--help' in sys.argv:
    sys.exit(0)
  try:
    myinp = sys.argv[1]
  except: myinp = None
  if myinp:
    rhost = myinp #XXX: should test rhost validity here... (how ?)
  else: pass # use default
  del myinp

  # get server to run from user
  import sys
  try:
    myinp = sys.argv[2]
  except: myinp = None
  if myinp:
    server = myinp #XXX: should test validity here... (filename)
  else: pass # use default
  del myinp

  # get remote port to run server on from user
  import sys
  try:
    myinp = sys.argv[3]
  except: myinp = None
  if myinp:
    rport = myinp #XXX: should test validity here... (filename)
  else: pass # use default
  del myinp

  # get remote profile (this should go away soon)
  import sys
  try:
    myinp = sys.argv[4]
  except: myinp = None
  if myinp:
    rprof = myinp #XXX: should test validity here... (filename)
    profiles = {rhost:rprof}
  else: pass # use default
  del myinp

  # my remote environment (should be auto-detected)
  register_profiles(profiles)
  profile = get_profile(rhost)

##### CONFIGURATION & INPUT ########################

  # run server
  rserver = serve(server,rhost,rport, profile=profile)
  response = rserver.response()
  if response:
    print(response)
    raise OSError('Failure to start server')

  # get server pid  #FIXME: launcher.pid is not pid(server)
  target = '[P,p]ython[^#]*'+server # filter w/ regex for python-based server
  try:
    pid = getpid(target, rhost)
  except OSError:
    print("Cleanup on host may be required...")
    raise

  # test server
  # XXX: add a simple one-liner...
  print("\nServer running at port=%s with pid=%s" % (rport,pid))
  import sys
  print('Press <Enter> to kill server')
  sys.stdin.readline()

  # stop server
  print(kill(pid,rhost))
# del rserver  #XXX: delete should run self.kill (?)


# EOF
