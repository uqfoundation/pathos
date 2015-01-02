#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2004  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Forked by: Mike McKerns (January 2004)
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2004-2015 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
"""
This module contains the base class for popen launchers, and describes
the popen launcher interface. The 'config' method can be overwritten
for pipe customization.  The launcher's 'launch' method can be overwritten
with a derived launcher's new execution algorithm. See the following for
an example of standard use.


Usage
=====

A typical call to a popen 'launcher' will roughly follow this example:

    >>> # instantiate the launcher
    >>> launcher = Launcher()
    >>>
    >>> # configure the launcher to stage the command
    >>> launcher(command='hostname')
    >>>
    >>> # execute the launch and retrieve the response
    >>> launcher.launch()
    >>> print launcher.response()
 
"""
__all__ = ['Launcher', 'LauncherException']

import os
import signal
import random
import string
from pyre.ipc.Selector import Selector
from pyre.components.Component import Component

class LauncherException(Exception):
    '''Exception for failure to launch a command'''
    pass

# broke backward compatability: 30/05/14 ==> replace base-class almost entirely
class Launcher(Component):
    """a popen-based launcher for parallel and distributed computing."""

    verbose = True

    class Inventory(Component.Inventory):

        import pyre.inventory

#       nodes = pyre.inventory.int("nodes", default=0)
#       nodelist = pyre.inventory.slice("nodelist")
        background = pyre.inventory.bool('background', default=False)
        stdin = pyre.inventory.inputFile('stdin')
        command = pyre.inventory.str('command')


    def __init__(self, name=None, **kwds):# facility="launcher"):
        """create a popen-launcher

Inputs:
    name        -- a unique identifier (string) for the launcher
    command     -- a command to send  [default = 'echo <name>']
    background  -- run in background  [default = False]
    stdin       -- file type object that should be used as a standard input
                   for the remote process.
        """
        """
Additionally, default values are set for 'inventory' class members:
    nodes       -- number of parallel/distributed nodes  [default = 0]
    nodelist    -- list of parallel/distributed nodes  [default = None]
        """
        name = ''.join(random.choice(string.ascii_letters) for i in range(16)) \
               if name is None else name
       #Component.__init__(self, name, facility="launcher")
        super(Launcher, self).__init__(name, facility='launcher')
#       self.nodes = 0
#       self.nodelist = None
        self.message = None
        self._response = None
        self._pid = 0
        self.config(**kwds)
        return

    def __repr__(self):
        return "Launcher('%s')" % self.message

#   def _configure(self): #FIXME: not used due to 'config'
##      self.nodes = self.inventory.nodes
##      self.nodelist = self.inventory.nodelist
#       self.background = self.inventory.background
#       self.stdin = self.inventory.stdin
#       self.command = self.inventory.command
#       return

    def config(self, **kwds):
        '''configure the launcher using given keywords:

(Re)configure the launcher for the following inputs:
    command     -- a command to send  [default = 'echo <name>']
    background  -- run in background  [default = False]
    stdin       -- file type object that should be used as a standard input
                   for the remote process.
        '''
        if self.message is None:
            self.inventory.command = 'echo %s' % self.name 
        for key, value in kwds.items():
            if key == 'command':
                self.inventory.command = value
            elif key == 'background':
                self.inventory.background = value
            elif key == 'stdin':
                self.inventory.stdin = value

        self._stdout = None
        self.message = self.inventory.command
        names=['command','background','stdin']
        return dict((i,getattr(self.inventory, i)) \
                for i in self.inventory.propertyNames() if i in names)

    def launch(self):
        '''launch a configured command'''
       #self._execStrategy(self.message)
        self._response = None
        self._execute()
        return

    def _execute(self):
       #'''execute the launch by piping the command, & saving the file object'''
        from subprocess import Popen, PIPE, STDOUT
        #XXX: what if saved list/dict of _stdout instead of just the one?
        #     could associated name/_pid and _stdout
        if self.inventory.background: #Spawn a background process 
            try:
                p = Popen(self.message, shell=True,
                          stdin=self.inventory.stdin, stdout=PIPE,
                          stderr=STDOUT, close_fds=True)
            except:
                raise LauncherException('failure to pipe: %s' % self.message)
            self._pid = p.pid #get fileobject pid
            self._stdout = p.stdout #save fileobject
        else:
            try:
                p = Popen(self.message, shell=True,
                          stdin=self.inventory.stdin, stdout=PIPE)
            except:
                raise LauncherException('failure to pipe: %s' % self.message)
            self._stdout = p.stdout
            self._pid = 0 #XXX: MMM --> or -1 ?
        return

    def response(self):
        '''Return the response from the launched process.
        Return None if no response was received yet from a background process.
        '''

        if self._stdout is None:
            raise LauncherException("'launch' is required after any reconfiguration")
        if self._response is not None: return self._response

        # when running in foreground _pid is 0 (may change to -1)
        if self._pid <= 0:
            self._response = self._stdout.read()
            return self._response
        
        # handle response from a background process
        def onData(selector, fobj):
            if self.verbose: print("in Launcher.response.onData")
            self._debug.log('on_remote')
            self._response = fobj.read()
            selector.state = False
            return

        def onTimeout(selector):
            selector.state = False
        
        sel = Selector()
        #sel._info.activate()
        sel.notifyOnReadReady(self._stdout, onData)
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
            if self.verbose: print('Kill pid=%d' % self._pid)
            os.kill(self._pid, signal.SIGTERM)
            os.waitpid(self._pid, 0)
            self._pid = 0
        return

    # interface
    __call__ = config
    pass


# version
# file copied from pythia-0.8 pyre.mpi.Launcher.py (svn:danse.us/pyre -r2)

# End of file 
