#!/usr/bin/env python
#
## XMLRPC Server class
# adapted from J. Kim's XMLRPC server class
# by mmckerns@caltech.edu

"""
<summary doc goes here>
"""

import os
import socket
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
import journal
from Server import Server #XXX: in pythia-0.6, was pyre.ipc.Server
from XMLRPCRequestHandler import XMLRPCRequestHandler
import util


class XMLRPCServer(Server, SimpleXMLRPCDispatcher):
    """ Example:
          s = XMLRPCServer(host, port)
          s.register_function(a_method)
          s.activate()
          s.serve()
    """

    def activate(self):
        """ Install callbacks """
        
        Server.activate(self)
        self._selector.notifyOnReadReady(self._socket, self._onConnection)
        self._selector.notifyWhenIdle(self._onSelectorIdle)

        
    def serve(self):
        """ Enter select loop """
        
        timeout = 5
        Server.serve(self, 5)


    def _marshaled_dispatch(self, data, dispatch_method = None):
        """ Overriding SimpleXMLRPCDispatcher._marshaled_dispatch()
        enhanced fault string
        """

        import xmlrpclib
        from xmlrpclib import Fault

        params, method = xmlrpclib.loads(data)

        # generate response
        try:
            if dispatch_method is not None:
                response = dispatch_method(method, params)
            else:
                response = self._dispatch(method, params)
            # wrap response in a singleton tuple
            response = (response,)
            response = xmlrpclib.dumps(response, methodresponse=1)
        except Fault, fault:
            fault.faultString = util.print_exc_info()
            response = xmlrpclib.dumps(fault)
        except:
            # report exception back to server
            response = xmlrpclib.dumps(
                xmlrpclib.Fault(1, "\n%s" % util.print_exc_info())
                )

        return response


    def _registerChild(self, pid, fromchild):
        """ Register a child process information so it can be retrieved
        on select events
        """
        
        self._activeProcesses[fromchild] = pid
        self._selector.notifyOnReadReady(fromchild,
                                         self._handleMessageFromChild)


    def _unRegisterChild(self, fd):
        """ Remove a child process from active process register """
        
        del self._activeProcesses[fd]


    def _handleMessageFromChild(self, selector, fd):
        """ Handler for message from a child process """
        
        line = fd.readline()
        if line[:4] == 'done':
            pid = self._activeProcesses[fd]
            os.waitpid(pid, 0)
        self._unRegisterChild(fd)


    def _onSelectorIdle(self, selector):
        return True


    def _installSocket(self, host, port):
        """ Prepare a listening socket """
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if port == 0: #Get a random port
            pick = util.portnumber(min=port, max=64*1024)
            while True:
                try:
                    port = pick()
                    s.bind((host, port))
                    break
                except socket.error:
                    continue
        else: #Designated port
            s.bind((host, port))
            
        s.listen(10)
        self._socket = s
        self.host = host
        self.port = port
        return
        
    def _onConnection(self, selector, fd):
        
        if isinstance(fd, socket.SocketType):
            return self._onSocketConnection(fd)
        return None


    def _onSocketConnection(self, socket):
        
        conn, addr = socket.accept()
        handler = XMLRPCRequestHandler(server=self, socket=conn)
        handler.handle()
        return True


    def __init__(self, host, port):
        
        Server.__init__(self)
        SimpleXMLRPCDispatcher.__init__(self,allow_none=False,encoding=None)

        self._installSocket(host, port)
        self._activeProcesses = {} #{ fd : pid }


if __name__ == '__main__':
    
    import os, time, xmlrpclib

    s = XMLRPCServer('', 0)
    print 'port=%d' % s.port
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
        s = xmlrpclib.ServerProxy('http://localhost:%d' % port)
        print '1 + 2 =', s.add(1, 2)
        print '3 + 4 =', s.add(3, 4)

# End of file
