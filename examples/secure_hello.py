#!/usr/bin/env python
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
    rhost = 'login.cacr.caltech.edu'
   #rhost = 'upgrayedd.danse.us'
   #rhost = 'shc-c.cacr.caltech.edu'

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
