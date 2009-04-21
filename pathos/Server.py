#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2004 All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 


class Server(object):


    def selector(self):
        return self._selector


    def deactivate(self):
        self._selector.state = False
        return

    
    def activate(self, onTimeout=None, selector=None):
        """configure the selector and install the timeout callback"""

        if selector is None:
            import pyre.ipc
            selector = pyre.ipc.selector()

        if onTimeout is not None:
            selector.notifyWhenIdle(onTimeout)

        self._selector = selector

        return


    def serve(self, timeout):
        self._selector.watch(timeout)
        return


    def __init__(self):
        self._selector = None
        return


# End of file
