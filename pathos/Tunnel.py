#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
#
# adapted from J. Kim & M. McKerns' Tunnel class
"""
This module contains the base class for secure tunnel connections, and
describes the pathos tunnel interface.  See the following for an example.


Usage
=====

A typical call to a pathos 'tunnel' will roughly follow this example:

    >>> # instantiate the tunnel, providing it with a unique identifier
    >>> tunnel = SSH_Tunnel('tunnel')
    >>>
    >>> # establish a tunnel to the remote host and port
    >>> remotehost = 'remote.host.edu'
    >>> remoteport = 12345
    >>> localport = tunnel.connect(remotehost, remoteport)
    >>> print "Tunnel connected at local port: ", tunnel._lport
    >>>
    >>> # pause script execution to maintain the tunnel (i.e. do something)
    >>> sys.stdin.readline()
    >>>
    >>> # tear-down the tunneled connection
    >>> tunnel.disconnect()
 
"""
__all__ = ['Tunnel','TunnelException']

import os
import signal
from pyre.components.Component import Component
from LauncherSSH import LauncherSSH

class TunnelException(Exception):
    '''Exception for failure to establish ssh tunnel'''
    pass

class Tunnel(Component):
    """
Base class for tunneled launchers for parallel and distributed computing.
    """
    #MINPORT = 49152    
    MINPORT = 1024 
    MAXPORT = 65535

    class Inventory(Component.Inventory):
        import pyre.inventory
        
        launcher = pyre.inventory.facility('launcher',
                                           default=LauncherSSH('launcher'))
    
    def connect(self, remotehost, remoteport, through=None):
        '''establish a secure shell tunnel between local and remote host

Input:
    host       -- remote hostname  [user@host:path is also valid]
    tunnelport -- remote port number

Additional Input:
    through    -- 'tunnel-through' hostname  [default = None]
        '''
        from pathos.portpicker import portnumber

        pick = portnumber(self.MINPORT, self.MAXPORT)
        while True:
            port = pick()
            if port < 0:
                raise TunnelException, 'No available local port'
            #print 'Trying port %d...' % port
            
            try:
                self._connect(port, remotehost, remoteport, through=through)
                #print 'SSH tunnel %d:%s:%d' % (port, remotehost, remoteport)
            except TunnelException, e:
                if e.args[0] == 'bind':
                    self.disconnect()
                    continue
                else:
                    self.__disconnect()
                    raise TunnelException, 'Connection failed'
                
            self.connected = True
            return port

    def disconnect(self):
        '''destroy the ssh tunnel'''
        #FIXME: grep (?) for self._tunnel, then kill the pid
        if self._pid > 0:
            print 'Kill ssh pid=%d' % self._pid
            os.kill(self._pid, signal.SIGTERM)
            os.waitpid(self._pid, 0)
            self.__disconnect()
        return

    def __disconnect(self):
        '''disconnect tunnel internals'''
        self._pid = 0
        self.connected = False
        self._tunnel = None
        self._lport = None
        self._rport = None
        return

    def __init__(self, name):
        '''create a ssh tunnel launcher

Takes one initial input:
    name        -- a unique identifier (string) for the launcher
        '''
        Component.__init__(self, name, 'sshtunnel')
        self._launcher = self.inventory.launcher
        self.__disconnect()
        return

    def __repr__(self):
        if not self.connected:
            return "Tunnel('%s')" % self.name
        return "Tunnel('ssh %s')" % self._tunnel

    def _connect(self, localport, remotehost, remoteport, through=None):
        options = '-q -N -L%d:%s:%d' % (localport, remotehost, remoteport)
        command = ''
        if through: rhost = through
        else: rhost = remotehost
        self._launcher.config(rhost=rhost, command=command,
                              options=options, background=True) #XXX: MMM
                             #options=options, background=False)
        self._launcher.launch()
        self._tunnel = options  #XXX: MMM
        self._lport = localport
        self._rport = remoteport
        self._pid = self._launcher.pid() #FIXME: should be tunnel_pid [pid()+1]
        line = self._launcher.response()
        if line:
            if line.startswith('bind'):
                raise TunnelException, 'bind'
            else:
                print line
                raise TunnelException, 'failure'
        return

if __name__ == '__main__':
    pass


# End of file
