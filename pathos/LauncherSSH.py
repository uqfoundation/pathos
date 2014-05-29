#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
#
# adapted from Mike McKerns' and June Kim's gsl SSHLauncher class
"""
This module contains the derived class for secure shell (ssh) launchers
See the following for an example.


Usage
=====

A typical call to a 'ssh launcher' will roughly follow this example:

    >>> # instantiate the launcher, providing it with a unique identifier
    >>> launcher = LauncherSSH('launcher')
    >>>
    >>> # configure the launcher to perform the command on the selected host
    >>> launcher.config(command='hostname', rhost='remote.host.edu')
    >>>
    >>> # execute the launch and retrieve the response
    >>> launcher.launch()
    >>> print launcher.response()
 
"""
__all__ = ['LauncherSSH']

import os
import signal
from pyre.ipc.Selector import Selector

from Launcher import Launcher
class LauncherSSH(Launcher):
    '''a remote process launcher using ssh'''

    def __init__(self, name, **kwds):
        '''create a ssh launcher

Takes one initial input:
    name        -- a unique identifier (string) for the launcher

Additional Inputs:
    rhost       -- hostname to recieve command [user@host is also valid]
    command     -- remotely launched command  [default = 'echo hello']
    launcher    -- remote service mechanism (i.e. ssh, rsh)  [default = 'ssh']
    options     -- remote service options (i.e. -v, -N, -L)  [default = '']
    background  -- run in background  [default = False]
    stdin       -- file type object that should be used as a standard input
                   for the remote process.
        '''
        '''Additional inputs (intended for internal use):
    fgbg        -- run in foreground/background  [default = 'foreground']

Default values are set for methods inherited from the base class:
    nodes       -- number of parallel/distributed nodes  [default = 0]
    nodelist    -- list of parallel/distributed nodes  [default = None]
        '''
       #Launcher.__init__(self, name)
        super(LauncherSSH, self).__init__(name)
        self.config(**kwds)
        return

    class Inventory(Launcher.Inventory):
        import pyre.inventory

        launcher = pyre.inventory.str('launcher', default='ssh')
        options = pyre.inventory.str('options', default='')
        rhost = pyre.inventory.str('rhost', default='localhost')
        command = pyre.inventory.str('command', default='echo hello')
       #fgbg = pyre.inventory.str('fgbg', default='foreground')
        background = pyre.inventory.bool('background', default=False)
        stdin = pyre.inventory.inputFile('stdin')
       #XXX: also inherits 'nodes' and 'nodelist'
        pass

   #def _configure(self):
   #    #FIXME: bypassing this with 'config'
   #    return

    def config(self, **kwds):
        '''configure a remote command using given keywords:

(Re)configure the copier for the following inputs:
    rhost       -- hostname to recieve command [user@host is also valid]
    command     -- remotely launched command  [default = 'echo hello']
    launcher    -- remote service mechanism (i.e. ssh, rsh)  [default = 'ssh']
    options     -- remote service options (i.e. -v, -N, -L)  [default = '']
    background  -- run in background  [default = False]
    stdin       -- file type object that should be used as a standard input
                   for the remote process.
        '''
        for key, value in kwds.items():
            if key == 'command':
                self.inventory.command = value
            elif key == 'rhost':
                self.inventory.rhost = value
            elif key == 'launcher':
                self.inventory.launcher = value
            elif key == 'options':
                self.inventory.options = value
            elif key == 'background':
                self.inventory.background = value
            elif key == 'stdin':
                self.inventory.stdin = value
            # backward compatability
            elif key == 'fgbg':
                value = True if value in ['bg','background'] else False
                self.inventory.background = value
        names = ['command','rhost','launcher','options','background','stdin']
        return {i:getattr(self.inventory, i) \
                for i in self.inventory.propertyNames() if i in names}

    def launch(self):
        '''launch a configured command'''
        command = '%s %s %s "%s"' % (self.inventory.launcher,
                                   self.inventory.options,
                                   self.inventory.rhost,
                                   self.inventory.command)
       #self._execStrategy(command)
        self._response = None
        self._execute(command)
        return

    def _execute(self, command):
       #'''execute the launch by piping the command, & saving the file object'''
        from subprocess import Popen, PIPE, STDOUT
        if self.inventory.background: #Spawn an ssh process 
            p = Popen(command, shell=True,
                      stdin=self.inventory.stdin, stdout=PIPE,
                      stderr=STDOUT, close_fds=True)
            self._pid = p.pid #get fileobject pid
            self._fromchild = p.stdout #save fileobject
        else:
            p = Popen(command, shell=True,
                      stdin=self.inventory.stdin, stdout=PIPE)
            self._fromchild = p.stdout
            self._pid = 0 #XXX: MMM --> or -1 ?
        return

    def response(self):
        '''Return the response from a remotely launched process.
        Return None if there was no response yet from a background process.
        '''

        if self._response is not None:  return self._response

        # when running in foreground _pid is 0 (may change to -1)
        if self._pid <= 0:
            self._response = self._fromchild.read()
            return self._response
        
        # handle response from a background process
        def onData(selector, fobj):
            print "in LauncherSSH.response.onData"
            self._debug.log('on_remote')
            self._response = fobj.read()
            selector.state = False
            return

        def onTimeout(selector):
            selector.state = False
        
        sel = Selector()
        #sel._info.activate()
        sel.notifyOnReadReady(self._fromchild, onData)
        sel.notifyWhenIdle(onTimeout)
        sel.watch(2.0)
        # reset _response to None to allow capture of a next response
        # from a background process
        return self._response

    def pid(self):
        '''get launcher pid'''
        return self._pid

    def kill(self):
        '''terminate the launcher'''
        if self._pid > 0:
            print 'Kill ssh pid=%d' % self._pid
            os.kill(self._pid, signal.SIGTERM)
            os.waitpid(self._pid, 0)
            self._pid = 0
        return

    # backward compatability
    stage = config
    pass


if __name__ == '__main__':
    pass


# End of file
