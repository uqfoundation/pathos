#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
"""
example of using the secure launch interface

To run: python secure_hello.py
"""

from pathos import SSH_Launcher


if __name__ == '__main__':
   #import journal

    # test command and remote host
    command1 = 'echo "hello from..."'
    command2 = 'hostname'
   #command3 = 'sleep 5' #XXX: buggy?
   #command3 = ''  #XXX: buggy ?
    rhost = 'localhost'
   #rhost = 'computer.cacr.caltech.edu'
   #rhost = 'foobar.danse.us'

    launcher = SSH_Launcher('LauncherSSH')
   #journal.debug('LauncherSSH').activate()
    launcher.stage(command=command1, rhost=rhost, fgbg='background')
    launcher.launch()
    print launcher.response()
    launcher.stage(command=command2, rhost=rhost, fgbg='background')
    launcher.launch()
    print launcher.response()
   #launcher.stage(command=command3, rhost=rhost, fgbg='foreground')
   #launcher.launch()
   #print launcher.response()


# End of file
