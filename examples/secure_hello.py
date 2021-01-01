#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2021 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE
"""
example of using the secure launch interface

To run: python secure_hello.py
"""

from pathos.secure import Pipe


if __name__ == '__main__':

    # test command and remote host
    command1 = 'echo "hello from..."'
    command2 = 'hostname'
   #command3 = 'sleep 5' #XXX: buggy?
   #command3 = ''  #XXX: buggy ?
    rhost = 'localhost'
   #rhost = 'computer.cacr.caltech.edu'
   #rhost = 'foobar.danse.us'

    launcher = Pipe('LauncherSSH')
    launcher(command=command1, host=rhost, background=False)
    launcher.launch()
    print(launcher.response())
    launcher(command=command2, host=rhost, background=False)
    launcher.launch()
    print(launcher.response())
   #launcher(command=command3, host=rhost, background=False)
   #launcher.launch()
   #print(launcher.response())


# End of file
