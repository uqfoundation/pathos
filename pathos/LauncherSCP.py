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
    >>> copier(source='~/foo.txt', destination='remote.host.edu:~')
    >>> copier.launch()
    >>>
    >>> # configure and launch the copied file to a new destination
    >>> copier(source='remote.host.edu:~/foo.txt', destination='.')
    >>> copier.launch()
    >>> print copier.response()
 
"""
__all__ = ['FileNotFound','LauncherSCP']

class FileNotFound(Exception):
    '''Exception for improper source or destination format'''
    pass

from Launcher import Launcher

# broke backward compatability: 30/05/14 ==> replace base-class almost entirely
class LauncherSCP(Launcher):
    '''a popen-based copier for parallel and distributed computing.'''

    def __init__(self, name=None, **kwds):
        '''create a copier

Inputs:
    name        -- a unique identifier (string) for the launcher
    source      -- hostname:path of original  [user@host:path is also valid]
    destination -- hostname:path for copy  [user@host:path is also valid]
    launcher    -- remote service mechanism (i.e. scp, cp)  [default = 'scp']
    options     -- remote service options (i.e. -v, -P)  [default = '']
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
        super(LauncherSCP, self).__init__(name)
        self.config(**kwds)
        return

    class Inventory(Launcher.Inventory):
        import pyre.inventory

        launcher = pyre.inventory.str('launcher', default='scp')
        options = pyre.inventory.str('options', default='')
        source = pyre.inventory.str('source', default='.')
        destination = pyre.inventory.str('destination', default='.')
       #fgbg = pyre.inventory.str('fgbg', default='foreground')
        pass

    def config(self, **kwds):
        '''configure the copier using given keywords:

(Re)configure the copier for the following inputs:
    source      -- hostname:path of original  [user@host:path is also valid]
    destination -- hostname:path for copy  [user@host:path is also valid]
    launcher    -- remote service mechanism (i.e. scp, cp)  [default = 'scp']
    options     -- remote service options (i.e. -v, -P)  [default = '']
    background  -- run in background  [default = False]
    stdin       -- file type object that should be used as a standard input
                   for the remote process.
        '''
        for key, value in kwds.items():
            if key == 'command':
                raise KeyError('command')
            elif key == 'source': #note: if quoted, can be multiple sources
                self.inventory.source = value
            elif key == 'destination':
                self.inventory.destination = value
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
        self.message = '%s %s %s %s' % (self.inventory.launcher,
                                        self.inventory.options,
                                        self.inventory.source,
                                        self.inventory.destination)
        self.inventory.command = self.message
        names=['source','destination','launcher','options','background','stdin']
        return dict((i,getattr(self.inventory, i)) \
                for i in self.inventory.propertyNames() if i in names)

    # interface
    __call__ = config
    pass


if __name__ == '__main__':
    pass


# End of file
