#!/usr/bin/env python
#
# Originally from pythia-0.8 pyre.mpi.Launcher.py (svn:danse.us/pyre -r2)
# Forked by: Mike McKerns (January 2004)
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2004-2015 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
"""
This module contains the base class for popen launchers, and describes
the popen launcher interface. The 'config' method can be overwritten
for pipe customization. The launcher's 'launch' method can be overwritten
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
import sys
import signal
import random
import string
from Selector import Selector

class LauncherException(Exception):
    '''Exception for failure to launch a command'''
    pass

# broke backward compatability: 30/05/14 ==> replace base-class almost entirely
class Launcher(object):
    """a popen-based launcher for parallel and distributed computing."""

    verbose = True
    from pathos import logger
    _debug = logger(level=30) # logging.WARN
    del logger


    def __init__(self, name=None, **kwds):
        """create a popen-launcher

Inputs:
    name        -- a unique identifier (string) for the launcher
    command     -- a command to send  [default = 'echo <name>']
    background  -- run in background  [default = False]
    stdin       -- file type object that should be used as a standard input
                   for the remote process.
        """
        xyz = string.ascii_letters
        self.name = ''.join(random.choice(xyz) for i in range(16)) \
               if name is None else name

        self.background = kwds.pop('background', False)
        self.stdin = kwds.pop('stdin', sys.stdin)
        self.message = kwds.pop('command', 'echo %s' % self.name) #' '?
        self._response = None
        self._pid = 0
        self.config(**kwds)
        return

    def __repr__(self):
        return "Launcher('%s')" % self.message

    def config(self, **kwds):
        '''configure the launcher using given keywords:

(Re)configure the launcher for the following inputs:
    command     -- a command to send  [default = 'echo <name>']
    background  -- run in background  [default = False]
    stdin       -- file type object that should be used as a standard input
                   for the remote process.
        '''
        if self.message is None:
            self.message = 'echo %s' % self.name  #' '?
        if self.stdin is None:
            self.stdin = sys.stdin
        for key, value in kwds.items():
            if key == 'command':
                self.message = value
            elif key == 'background':
                self.background = value
            elif key == 'stdin':
                self.stdin = value

        self._stdout = None
        names=['message','background','stdin']
        return dict((i,getattr(self, i)) for i in names)

    def launch(self):
        '''launch a configured command'''
        self._response = None
        self._execute()
        return

    def _execute(self):
       #'''execute by piping the command, & saving the file object'''
        from subprocess import Popen, PIPE, STDOUT
        #XXX: what if saved list/dict of _stdout instead of just the one?
        #     could associated name/_pid and _stdout
        if self.background: #Spawn a background process 
            try:
                p = Popen(self.message, shell=True,
                          stdin=self.stdin, stdout=PIPE,
                          stderr=STDOUT, close_fds=True)
            except:
                raise LauncherException('failure to pipe: %s' % self.message)
            self._pid = p.pid #get fileobject pid
            self._stdout = p.stdout #save fileobject
        else:
            try:
                p = Popen(self.message, shell=True,
                          stdin=self.stdin, stdout=PIPE)
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
            if self.verbose: print("handling launcher response")
            self._debug.info('on_remote')
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


# End of file 
