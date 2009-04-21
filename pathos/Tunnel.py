#!/usr/bin/env python
#
## ssh Tunnel class
# adapted from J. Kim & M. McKerns' Tunnel class
# by mmckerns@caltech.edu

"""
<summary doc goes here>
"""

import os
import signal
from pyre.components.Component import Component
from LauncherSSH import LauncherSSH

class TunnelException(Exception):
    pass

class Tunnel(Component):
    #MINPORT = 49152    
    MINPORT = 1024 
    MAXPORT = 65535

    class Inventory(Component.Inventory):
        import pyre.inventory
        
        launcher = pyre.inventory.facility('launcher',
                                           default=LauncherSSH('launcher'))
    
    def connect(self, remotehost, remoteport):
        import util

        pick = util.portnumber(self.MINPORT, self.MAXPORT)
        while True:
            port = pick()
            if port < 0:
                raise TunnelException, 'No available local port'
            print 'Trying port %d...' % port
            
            try:
                self._connect(port, remotehost, remoteport)
                print 'SSH tunnel %d:%s:%d' % (port, remotehost, remoteport)
            except TunnelException, e:
                if e.args[0] == 'bind':
                    self.disconnect()
                    continue
                else:
                    self._pid = 0
                    self.connected = False
                    raise TunnelException, 'Connection failed'
                
            self.connected = True
            return port

    def disconnect(self):
        if self._pid > 0:
            print 'Kill ssh pid=%d' % self._pid
            os.kill(self._pid, signal.SIGTERM)
            os.waitpid(self._pid, 0)
            self.connected = False
            self._pid = 0
        return

    def __init__(self, name):
        Component.__init__(self, name, 'sshtunnel')

        self._launcher = self.inventory.launcher
        
        self.connected = False

        self._pid = 0
        return

    def _connect(self, localport, remotehost, remoteport):
        options = '-N -L%d:%s:%d' % (localport, remotehost, remoteport)
        command = ''

        self._launcher.stage(rhost=remotehost, command=command,
                             options=options, fgbg='background')
        self._launcher.launch()
        self._pid = self._launcher.pid()
        line = self._launcher.response()
        if line:
            if line.startswith('bind'):
                raise TunnelException, 'bind'
            else:
                print line
                raise TunnelException, 'failure'
        return

if __name__ == '__main__':
    import sys

    t = Tunnel('Tunnel')
    port = t.connect('login.cacr.caltech.edu', 23)
    print 'Local port:', port
    print 'Press <Enter> to disconnect'
    sys.stdin.readline()
    t.disconnect()
