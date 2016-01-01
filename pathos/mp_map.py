#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
"""
minimal interface to python's multiprocessing module
"""

from pathos.multiprocessing import ProcessPool, __STATE
from pathos.threading import ThreadPool #XXX: thread __STATE not imported
from pathos.helpers import cpu_count
mp = ProcessPool()
tp = ThreadPool()

# backward compatibility
#FIXME: deprecated... and buggy!  (fails to dill on imap/uimap)
def mp_map(function, sequence, *args, **kwds):
    '''extend python's parallel map function to multiprocessing

Inputs:
    function  -- target function
    sequence  -- sequence to process in parallel

Additional Inputs:
    nproc     -- number of 'local' cpus to use  [defaut = 'autodetect']
    type      -- processing type ['blocking', 'non-blocking', 'unordered']
    threads   -- if True, use threading instead of multiprocessing
    '''
    processes = cpu_count()
    proctype = 'blocking'
    threads = False
    if kwds.has_key('nproc'):
        processes = kwds['nproc']
        kwds.pop('nproc')
        # provide a default that is not a function call
        if processes == None: processes = cpu_count()
    if kwds.has_key('type'):
        proctype = kwds['type']
        kwds.pop('type')
    if kwds.has_key('threads'):
        threads = kwds['threads']
        kwds.pop('threads')
    # remove all the junk kwds that are added due to poor design!
    if kwds.has_key('nnodes'): kwds.pop('nnodes')
    if kwds.has_key('nodes'): kwds.pop('nodes')
    if kwds.has_key('launcher'): kwds.pop('launcher')
    if kwds.has_key('mapper'): kwds.pop('mapper')
    if kwds.has_key('queue'): kwds.pop('queue')
    if kwds.has_key('timelimit'): kwds.pop('timelimit')
    if kwds.has_key('scheduler'): kwds.pop('scheduler')
    if kwds.has_key('ncpus'): kwds.pop('ncpus')
    if kwds.has_key('servers'): kwds.pop('servers')

    if proctype in ['blocking']:
        if not threads:
            return mp.map(function,sequence,*args,**kwds)
        else:
            return tp.map(function,sequence,*args,**kwds)
    elif proctype in ['unordered']:
        if not threads:
            return mp.uimap(function,sequence,*args,**kwds)
        else:
            return tp.uimap(function,sequence,*args,**kwds)
    elif proctype in ['non-blocking', 'ordered']:
        if not threads:
            return mp.imap(function,sequence,*args,**kwds)
        else:
            return tp.imap(function,sequence,*args,**kwds)
    # default
    if not threads:
        return mp.map(function,sequence,*args,**kwds)
    else:
        return tp.map(function,sequence,*args,**kwds)



if __name__ == '__main__':
  pass

