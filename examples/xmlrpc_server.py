#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE
"""
example of building a simple xmlrpc server and proxy,
and then demonstrate the handling of a few basic requests

To run: python xmlrpc_server.py
To stop: < Ctrl+C >
"""

from pathos.xmlrpc import XMLRPCServer
from pathos import logger
logger(level=20, name='pathos.xmlrpc')   # logging.INFO
logger(level=20, name='pathos.selector') # logging.INFO

if __name__ == '__main__':
    
    import os, time
    import xmlrpc.client as client

    s = XMLRPCServer('', 0)
    print('port=%d' % s.port)
    port = s.port

    pid = os.fork()
    if pid > 0: #parent
        def add(x, y): return x + y
        s.register_function(add)
        s.activate()
        #s._selector._info.activate()
        s.serve()
    else: #child
        time.sleep(1)
        s = client.ServerProxy('http://localhost:%d' % port)
        print('1 + 2 = %s' % s.add(1, 2))
        print('3 + 4 = %s' % s.add(3, 4))

# End of file
