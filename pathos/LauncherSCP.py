#!/usr/bin/env python
#
## scp Launcher class
# adapted from Mike McKerns' gsl SCPLauncher class
# by mmckerns@caltech.edu

"""
<summary doc goes here>
"""

import os
import popen2

class FileNotFound(Exception):
    '''Exception for improper source or destination format'''
    pass


from Launcher import Launcher
class LauncherSCP(Launcher):
    '''a remote copier using scp'''

    def __init__(self, name, **kwds):
        '''create a scp launcher

Inputs:
    name    - a (string) name for the launcher

Optional Inputs:
    Any of the `stage` method's keywords can be passed during
    initialization to override the launcher defualts. 
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
       #XXX: also inherits 'nodes' and 'nodelist'
        pass

   #def _configure(self):
   #    #FIXME: bypassing this with 'stage'
   #    return

    def stage(self, **kwds):
        '''stage a remote copy using given keywords:
    source = hostname:path of original [user@host:path is also valid]
    destination = hostname:path for copy [user@host:path is also valid]
    launcher = remote service mechanism (i.e. scp, cp)
    options = remote service options (i.e. -v, -P)
    fgbg = run in foreground/background
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
        return

    def launch(self):
        '''launch a staged command'''
        command = '%s %s %s %s' % (self.inventory.launcher,
                                   self.inventory.options,
                                   self.inventory.source,
                                   self.inventory.destination)
       #self._execStrategy(command)
        self._execute(command)
        return

    def _execute(self, command):
        '''execute the launch by piping the command, & saving the file object'''
        if self.inventory.fgbg in ['foreground','fg']:
            f = os.popen(command, 'r')
            self._fromchild = f #save fileobject
        else: #Spawn an scp process 
            p = popen2.Popen4(command)
            self._pid = p.pid #get fileobject pid
            self._fromchild = p.fromchild #save fileobject
        return

    def pid(self):
        '''get copier pid'''
        return self._pid
    pass


if __name__=='__main__':
    pass


# End of file 
