#!/usr/bin/env python
"""
high-level programming interface to core pathos utilities
"""

import os
import logging

def copy(filename, rhost, dest):
  '''copy 'file' object to target destination

Inputs:
    filename    -- path string of source 'file'
    rhost       -- hostname of destination target
    destination -- path string for destination target
  '''
  from LauncherSCP import LauncherSCP
  copier = LauncherSCP('copy_%s' % filename)
  logging.info('executing {scp %s %s:%s}', filename, rhost, dest)
  copier.stage(options='-q', source=filename, destination=rhost+':'+dest)
  copier.launch()
  return


def run(command,rhost,bg=True): #XXX: default should be fg=True ?
  '''execute a command on a remote host

Inputs:
    command -- command string to be executed
    host    -- hostname of execution target
    bg      -- run as background process?  [default = True]
  '''
  if not bg: fgbg = 'foreground'
  else: fgbg = 'background'
  from LauncherSSH import LauncherSSH
  launcher = LauncherSSH('%s' % command)
  logging.info('executing {ssh %s "%s"}', rhost, command)
  launcher.stage(options='-q', command=command, rhost=rhost, fgbg=fgbg)
  launcher.launch()
  return launcher.response() #XXX: should return launcher, not just response


def kill(pid,rhost): #XXX: launcher has a method to "kill self", why not use it?
  '''kill a process on a remote host

Inputs:
    pid   -- process id
    rhost -- hostname where process is running
  '''
  command = 'kill -n TERM %s' % pid #XXX: TERM=15 or KILL=9 ?
  return run(command,rhost,bg=False)


def getpid(target,rhost): #XXX: or 'ps -j' for pid, ppid, pgid ?
  '''get the process id for a target process running on a remote host

NOTE: This method should only be used as a last-ditch effort to kill a process.
This method _may_ work when a child has been spawned and the pid was not
registered... but there's no guarantee.

Inputs:
    target -- string name of target process
    rhost  -- hostname where process is running
  '''
 #command = "ps -A | grep '%s'" % target #XXX: 'other users' only
  command = "ps ax | grep '%s'" % target #XXX: 'all users'
  logging.info('executing {ssh %s "%s"}', rhost, command)
  response = run(command,rhost)
  pid = response.split(" ")[0:2] # pid is 1st or 2nd element of response string
  return pid[0] or pid[1]


def pickport(rhost):
  '''select a open port on a remote host

Inputs:
    rhost -- hostname on which to select a open port
  '''
  from pathos.LauncherSSH import LauncherSSH
  from pathos.portpicker import __file__ as src
  # make sure src is a .py file, not .pyc or .pyo
  src = src.rstrip('co')
  launcher = LauncherSSH('pickport')
  launcher.stage(command='python', rhost=rhost,
          fgbg='foreground', stdin=open(src))
  logging.info('executing {python <%s} on %s', src, rhost)
  launcher.launch()
  try:
    rport = int(launcher.response())
  except:
    from Tunnel import TunnelException
    raise TunnelException, "failure to pick remote port"
  # return remote port number
  return rport


def connect(rhost,rport):
  '''establish a secure tunnel connection to a remote host at the given port

Inputs:
    rhost  -- hostname to which a tunnel should be established
    rport  -- port number (on rhost) to connect the tunnel to
  '''
  from Tunnel import Tunnel
  t = Tunnel('Tunnel')
  lport = t.connect(rhost,rport)
  #FIXME: want to have r.lport, r.rport, r.rhost as class members
  return t,lport


def serve(server,rhost,rport,profile='.bash_profile'):
  '''begin serving RPC requests

Inputs:
    server  -- name of RPC server  (i.e. 'ppserver')
    rhost   -- hostname on which a server should be launched
    rport   -- port number (on rhost) that server will accept request at
    profile -- file on remote host that instantiates the user's environment
        [default = '.bash_profile']
  '''
  file = '~/bin/%s.py' % server  #XXX: _should_ be on the $PATH
  #file = '%s.py' % server
  command = "source %s; %s -p %s" % (profile,file,rport)
  from LauncherSSH import LauncherSSH
  rserver = LauncherSSH('%s' % command)
  logging.info('executing {ssh %s "%s"}', rhost, command)
  rserver.stage(options='-q', command=command, rhost=rhost, fgbg='background')
  rserver.launch()
  response = rserver.response()
  logging.info('response = %r', response)
  if response in ['', None]: #XXX: other responses allowed (?)
    pass
  else:
    logging.error('invalid response = %r', response) #XXX: not really error checking...
  from time import sleep
  delay = 2.0
  sleep(delay)
  return response


if __name__ == '__main__':
  pass

