#!/usr/bin/env/python
"""
This module contains map and pipe interfaces to standard (i.e. serial) python.

Pipe methods provided:
    pipe        - blocking communication pipe             [returns: value]

Map methods provided:
    map         - blocking and ordered worker pool      [returns: list]
    imap        - non-blocking and ordered worker pool  [returns: iterator]


Usage
=====

A typical call to a pathos python map will roughly follow this example:

    >>> # instantiate and configure the worker pool
    >>> from pathos.python import PythonSerial
    >>> pool = PythonSerial()
    >>>
    >>> # do a blocking map on the chosen function
    >>> results = pool.map(pow, [1,2,3,4], [5,6,7,8])
    >>>
    >>> # do a non-blocking map, then extract the results from the iterator
    >>> results = pool.imap(pow, [1,2,3,4], [5,6,7,8])
    >>> results = list(results)


Notes
=====

This worker pool leverages the built-in python maps, and thus does not have
limitations due to serialization of the function f or the sequences in args.
The maps in this worker pool have full functionality whether run from a script
or in the python interpreter, and work reliably for both imported and
interactively-defined functions.

"""
__all__ = ['PythonSerial']

from pathos.abstract_launcher import AbstractWorkerPool
__get_nodes__ = AbstractWorkerPool._AbstractWorkerPool__get_nodes
__set_nodes__ = AbstractWorkerPool._AbstractWorkerPool__set_nodes
from itertools import imap as _imap
from __builtin__ import map as _map, apply as _apply

class PythonSerial(AbstractWorkerPool):
    """
Mapper that leverages standard (i.e. serial) python maps.
    """
    def map(self, f, *args, **kwds):
       #AbstractWorkerPool._AbstractWorkerPool__map(self, f, *args, **kwds)
        return _map(f, *args)#, **kwds)
    map.__doc__ = AbstractWorkerPool.map.__doc__
    def imap(self, f, *args, **kwds):
       #AbstractWorkerPool._AbstractWorkerPool__imap(self, f, *args, **kwds)
        return _imap(f, *args)#, **kwds)
    imap.__doc__ = AbstractWorkerPool.imap.__doc__
    ########################################################################
    # PIPES
    def pipe(self, f, *args, **kwds):
       #AbstractWorkerPool._AbstractWorkerPool__pipe(self, f, *args, **kwds)
        return _apply(f, args, kwds)
    pipe.__doc__ = AbstractWorkerPool.pipe.__doc__
    #XXX: generator/yield provides simple ipipe? apipe? what about coroutines?
    ########################################################################
    # interface
    __get_nodes = __get_nodes__
    __set_nodes = __set_nodes__
    nodes = property(__get_nodes, __set_nodes)
    pass


