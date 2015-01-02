#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2015 California Institute of Technology.
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
    >>> launcher(command='hostname', host='remote.host.edu')
    >>>
    >>> # execute the launch and retrieve the response
    >>> launcher.launch()
    >>> print launcher.response()
 
"""
__all__ = ['LauncherSSH']

from Launcher import Launcher

# broke backward compatability: 30/05/14 ==> replace base-class almost entirely
class LauncherSSH(Launcher):
    '''a popen-based ssh-launcher for parallel and distributed computing.'''

    def __init__(self, name=None, **kwds):
        '''create a ssh launcher

Inputs:
    name        -- a unique identifier (string) for the launcher
    host        -- hostname to recieve command [user@host is also valid]
    command     -- a command to send  [default = 'echo <name>']
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
        host = pyre.inventory.str('host', default='localhost')
       #fgbg = pyre.inventory.str('fgbg', default='foreground')
        pass

   #def _configure(self):
   #    #FIXME: bypassing this with 'config'
   #    return

    def config(self, **kwds):
        '''configure a remote command using given keywords:

(Re)configure the copier for the following inputs:
    host        -- hostname to recieve command [user@host is also valid]
    command     -- a command to send  [default = 'echo <name>']
    launcher    -- remote service mechanism (i.e. ssh, rsh)  [default = 'ssh']
    options     -- remote service options (i.e. -v, -N, -L)  [default = '']
    background  -- run in background  [default = False]
    stdin       -- file type object that should be used as a standard input
                   for the remote process.
        '''
        if self.message is None:
            self.inventory.command = 'echo %s' % self.name 
        for key, value in kwds.items():
            if key == 'command':
                self.inventory.command = value
            elif key == 'host':
                self.inventory.host = value
            elif key == 'launcher':
                self.inventory.launcher = value
            elif key == 'options':
                self.inventory.options = value
            elif key == 'background':
                self.inventory.background = value
            elif key == 'stdin':
                self.inventory.stdin = value
            # backward compatability
           #elif key == 'fgbg':
           #    value = True if value in ['bg','background'] else False
           #    self.inventory.background = value

        self._stdout = None
        self.message = '%s %s %s "%s"' % (self.inventory.launcher,
                                          self.inventory.options,
                                          self.inventory.host,
                                          self.inventory.command)
        names = ['command','host','launcher','options','background','stdin']
        return dict((i,getattr(self.inventory, i)) \
                for i in self.inventory.propertyNames() if i in names)

    # interface
    __call__ = config
    pass


if __name__ == '__main__':
    pass


# End of file
