#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
#
# adapted from Mike McKerns' gsl SCPLauncher class
"""
This module contains the derived class for launching secure copy (scp)
commands.  See the following for an example.


Usage
=====

A typical call to a 'scp launcher' will roughly follow this example:

    >>> # instantiate the launcher, providing it with a unique identifier
    >>> copier = LauncherSCP('copier')
    >>>
    >>> # configure and launch the copy to the selected destination
    >>> copier.stage(source='~/foo.txt', destination='remote.host.edu:~')
    >>> copier.launch()
    >>>
    >>> # configure and launch the copied file to a new destination
    >>> copier.stage(source='remote.host.edu:~/foo.txt', destination='.')
    >>> copier.launch()
    >>> print copier.response()
 
"""
__all__ = ['FileNotFound','LauncherSCP']

class FileNotFound(Exception):
    '''Exception for improper source or destination format'''
    pass

import os
import signal
from pyre.ipc.Selector import Selector

from Launcher import Launcher
class LauncherSCP(Launcher):
    '''a remote copier using scp'''

    def __init__(self, name, **kwds):
        '''create a scp launcher

Takes one initial input:
    name        -- a unique identifier (string) for the launcher

Additional Inputs:
    source      -- hostname:path of original  [user@host:path is also valid]
    destination -- hostname:path for copy  [user@host:path is also valid]
    launcher    -- remote service mechanism (i.e. scp, cp)  [default = 'scp']
    options     -- remote service options (i.e. -v, -P)  [default = '']
    fgbg        -- run in foreground/background  [default = 'foreground']

Default values are set for methods inherited from the base class:
    nodes       -- number of parallel/distributed nodes  [default = 0]
    nodelist    -- list of parallel/distributed nodes  [default = None]
        '''
       #Launcher.__init__(self, name)
        super(LauncherSCP, self).__init__(name)
        self.stage(**kwds)
        return

    class Inventory(Launcher.Inventory):
        import pyre.inventory

        launcher = pyre.inventory.str('launcher', default='scp')
        options = pyre.inventory.str('options', default='')
        source = pyre.inventory.str('source', default='')
        destination = pyre.inventory.str('destination', default='')
        fgbg = pyre.inventory.str('fgbg', default='foreground')
        stdin = pyre.inventory.inputFile('stdin')
       #XXX: also inherits 'nodes' and 'nodelist'
        pass

   #def _configure(self):
   #    #FIXME: bypassing this with 'stage'
   #    return

    def stage(self, **kwds):
        '''stage a remote copy

(Re)configure the copier for the following inputs:
    source      -- hostname:path of original  [user@host:path is also valid]
    destination -- hostname:path for copy  [user@host:path is also valid]
    launcher    -- remote service mechanism (i.e. scp, cp)  [default = 'scp']
    options     -- remote service options (i.e. -v, -P)  [default = '']
    fgbg        -- run in foreground/background  [default = 'foreground']
    stdin       -- file type object that should be used as a standard input
                   for the remote process.
        '''
        for key, value in kwds.items():
            if key == 'source': #note: if quoted, can be multiple sources
                self.inventory.source = value
            elif key == 'destination':
                self.inventory.destination = value
            elif key == 'launcher':
                self.inventory.launcher = value
            elif key == 'options':
                self.inventory.options = value
            elif key == 'fgbg':
                self.inventory.fgbg = value
            elif key == 'stdin':
                self.inventory.stdin = value
        return

    def launch(self):
        '''launch a staged command'''
        command = '%s %s %s %s' % (self.inventory.launcher,
                                   self.inventory.options,
                                   self.inventory.source,
                                   self.inventory.destination)
       #self._execStrategy(command)
        self._response = None
        self._execute(command)
        return

    def _execute(self, command):
       #'''execute the launch by piping the command, & saving the file object'''
        from subprocess import Popen, PIPE, STDOUT
        if self.inventory.fgbg in ['foreground','fg']:
            p = Popen(command, shell=True,
                      stdin=self.inventory.stdin, stdout=PIPE)
            self._fromchild = p.stdout
            self._pid = 0 #XXX: MMM --> or -1 ?
        else: #Spawn an scp process 
            p = Popen(command, shell=True,
                      stdin=self.inventory.stdin, stdout=PIPE,
                      stderr=STDOUT, close_fds=True)
            self._pid = p.pid #get fileobject pid
            self._fromchild = p.stdout #save fileobject
           #self._fromchild = p.fromchild #save fileobject
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
            print "in LauncherSCP.response.onData"
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
        '''get copier pid'''
        return self._pid

    def kill(self):
        '''terminate the launcher'''
        if self._pid > 0:
            print 'Kill scp pid=%d' % self._pid
            os.kill(self._pid, signal.SIGTERM)
            os.waitpid(self._pid, 0)
            self._pid = 0
        return
    pass


if __name__=='__main__':
    pass


# End of file 
