#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
"""
high-level programming interface to core pathos utilities
"""
__all__ = ['copy', 'execute', 'kill', 'getpid', 'getppid', 'getchild', \
           'serve', 'connect', 'randomport']

import os
import string
import logging
import re

# standard pattern for 'ps axj': '... ddddd ddddd ddddd ...'
_psaxj = re.compile("((\S+\s+)?\d+\s+\d+\s+\d+\s)")


def copy(source, destination):
  '''copy source to (possibly) remote destination

Execute a copy, and return the copier. Use 'kill' to kill the copier, and 
'pid' to get the process id for the copier.

Inputs:
    source      -- path string of source 'file'
    destination -- path string for destination target
  '''
  from LauncherSCP import LauncherSCP
  copier = LauncherSCP()
  if ':' in source or ':' in destination:
    copier(options='-q -r', source=source, destination=destination)
  else:
    copier(launcher='cp', options='-r', source=source, destination=destination)
  logging.info('executing {%s}', copier.message)
  copier.launch()
  copier.kill()
  return copier


def execute(command, host=None, bg=True):
  '''execute a command (possibly) on a remote host

Execute a process, and return the launcher. Use 'response' to retrieve the
response from the executed command. Use 'kill' to kill the launcher, and 'pid'
to get the process id for the launcher.

Inputs:
    command -- command string to be executed
    host    -- hostname of execution target  [default = None (i.e. run locally)]
    bg      -- run as background process?  [default = True]
  '''
  bg = bool(bg)
  if host in [None, '']:
    from Launcher import Launcher
    launcher = Launcher()
    launcher(command=command, background=bg)
  else:
    from LauncherSSH import LauncherSSH
    launcher = LauncherSSH()
    launcher(options='-q', command=command, host=host, background=bg)
  logging.info('executing {%s}', launcher.message)
  launcher.launch()
 #response = launcher.response()
 #launcher.kill()
 #return response
  return launcher


#XXX: add local-only equivalents for kill and *pid to pox?
def kill(pid, host=None): #XXX: launcher "kill self" method; use it?
  '''kill a process (possibly) on a remote host

Inputs:
    pid   -- process id
    host  -- hostname where process is running [default = None (i.e. locally)]
  '''
  command = 'kill -n TERM %s' % pid #XXX: TERM=15 or KILL=9 ?
  return execute(command, host, bg=False).response()
  #XXX: raise OSError('[Errno 3] No such process') when no process found ?


def _psax(response, pattern=None):
  """strips out bad lines in 'ps ax' response

  Takes multi-line string, response from execute('ps ax') or execute('ps axj').
  Takes an optional regex pattern for finding 'good' lines.  If pattern
  is None, assumes 'ps ax' was called.
  """
  if not response: return response
  if pattern:
    response = (line for line in response.split('\n') if pattern.match(line))
  else: # a 'ps ax' line should start with a 'digit'; " PID THING ..."
    response = (line for line in response.split('\n') \
                                 if line and line.lstrip()[0] in string.digits)
  return '\n'.join(response)


def getpid(target=None, host=None):
  '''get the process id for a target process (possibly) running on remote host

This method should only be used as a last-ditch effort to find a process id.
This method __may__ work when a child has been spawned and the pid was not
registered... but there's no guarantee.

If target is None, then get the process id of the __main__  python instance.

Inputs:
    target -- string name of target process
    host   -- hostname where process is running
  '''
  if target is None:
    return None if host else os.getpid()
 #command = "ps -A | grep '%s'" % target # 'other users' only
  command = "ps ax | grep '%s'" % target # 'all users'
  response = _psax(execute(command, host, bg=False).response())
  ignore = "grep '%s'" % target
  try: # select the PID
    # find most recent where "grep '%s'" not in line
    pid = sorted(_select(line,(0,))[0] \
          for line in response.split('\n') if line and ignore not in line)
    if pid is None:
      raise OSError('Failure to recover process id')
    #XXX: take advantage of *ppid to help match correct pid?
    return int(pid[-1])
  except (AttributeError, IndexError):
    raise OSError('[Error 3] No such process')


def _select(line, indx):
  '''select the correct data from the string, using the given index

  Takes a single string line, and a tuple of positional indicies.
  '''
  line = line.split()
  if max(indx) > len(line) - 1:
    return (None,None) # for the off chance there's a bad line
  return tuple(line[i] for i in indx)


def getppid(pid=None, host=None, group=False): # find parent of pid
  '''get parent process id (ppid) for the given process

If pid is None, the pid of the __main__  python instance will be used.

Inputs:
    pid    -- process id
    host   -- hostname where process is running
    group  -- get parent group id (pgid) instead of direct parent id?
  '''
  if pid is None:
    return None if host else os.getpgrp() if group else os.getppid()
  pid = str(pid)
  command = "ps axj"
  response = execute(command, host).response()
  # analyze header for correct pattern and indx
  head = (line for line in response.split('\n') if 'PPID' in line)
  try: head = head.next().split()
  except StopIteration: return None
  parent = 'PGID' if group else 'PPID'
  indx = (head.index('PID'), head.index(parent))
  # extract good data lines from response
  response = _psax(response, pattern=_psaxj)
  # select the PID and parent id
  response = dict(_select(line,indx) for line in response.split('\n') if line)
  response = response.get(pid, None)
  return None if response is None else int(response)
  #XXX: raise OSError('[Errno 3] No such process') when no process found ?


def getchild(pid=None, host=None, group=False): # find all children of pid
  '''get all child process ids for the given parent process id (ppid)

If pid is None, the pid of the __main__  python instance will be used.

Inputs:
    pid    -- parent process id
    host   -- hostname where process is running
    group  -- get process ids for the parent group id (pgid) instead?
  '''
  if pid is None:
    if host: return None
    pid = getpid()
  pid = str(pid)
  command = "ps axj"
  response = execute(command, host).response()
  # analyze header for correct pattern and indx
  head = (line for line in response.split('\n') if 'PPID' in line)
  try: head = head.next().split()
  except StopIteration: return []
  parent = 'PGID' if group else 'PPID'
  indx = (head.index('PID'), head.index(parent))
  # extract good data lines from response
  response = _psax(response, pattern=_psaxj)
  # select the PID and parent id
  response = dict(_select(line,indx) for line in response.split('\n') if line)
  return [int(key) for (key,value) in response.items() if value == pid]
  #XXX: raise OSError('[Errno 3] No such process') when no process found ?


def randomport(host=None):
  '''select a open port on a (possibly) remote host

Inputs:
    host -- hostname on which to select a open port
  '''
  from pathos.portpicker import randomport
  if not host:
    return randomport()
  from pathos.LauncherSSH import LauncherSSH
  from pathos.portpicker import __file__ as src
  # make sure src is a .py file, not .pyc or .pyo
  src = src.rstrip('co')
  launcher = LauncherSSH() #XXX: use pox.which / which_python?
  launcher(command='python', host=host, background=False, stdin=open(src))
  logging.info('executing {python <%s} on %s', src, host)
  launcher.launch()
  try:
    rport = int(launcher.response())
  except:
    from Tunnel import TunnelException
    raise TunnelException("failure to pick remote port")
  # return remote port number
  return rport


def connect(host, port=None):
  '''establish a secure tunnel connection to a remote host at the given port

Inputs:
    host  -- hostname to which a tunnel should be established
    port  -- port number (on host) to connect the tunnel to
  '''
  from Tunnel import Tunnel
  t = Tunnel('connect') #FIXME: better default (i.e. don't give a name)
  if port is None: port = randomport(host)
  t.connect(host, port)
  return t


def serve(server, host=None, port=None, profile='.bash_profile'):
  '''begin serving RPC requests

Inputs:
    server  -- name of RPC server  (i.e. 'ppserver')
    host    -- hostname on which a server should be launched
    port    -- port number (on host) that server will accept request at
    profile -- file on remote host that instantiates the user's environment
        [default = '.bash_profile']
  '''
  if host is None: #XXX: and...?
    profile = ''
  else:
    profile = 'source %s; ' % profile
  file = '~/bin/%s.py' % server  #XXX: _should_ be on the $PATH
  if port is None: port = randomport(host)
  command = "%s -p %s" % (file,port)
  rserver = execute(command, host, bg=True)
  response = rserver.response()
  logging.info('response = %r', response)
  if response in ['', None]: #XXX: other responses allowed (?)
    pass
  else: #XXX: not really error checking...
    logging.error('invalid response = %r', response)
  from time import sleep
  delay = 2.0
  sleep(delay)
  return rserver


if __name__ == '__main__':
  pass

