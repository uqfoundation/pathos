#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
"""
demonstrates use of the pathos profiler

inspired by: http://stackoverflow.com/a/32522579/4646678
"""
from pathos.helpers import mp
import time
import random
try:
    from itertools import imap as map
except ImportError:
    pass

from pathos.profile import *


if __name__ == '__main__':

    config = dict(gen=process_id)

   #@profiled(**config)
    def _work(i):
        x = random.random()
        time.sleep(x)
        return (i,x)

    work = profiled(**config)(_work)

    """
    # create a profiling pool
    mpPool = profiling(mp.Pool)
    pool = mpPool(10)
    #XXX: ALT: pool = mp.Pool(10, enable_profiling)

    for i in pool.imap_unordered(work, range(100)):
        print(i)
    """

    enable_profiling()
    
    """
    # profile the work (not the map internals) in the main thread
    for i in map(work, range(-10,0)):
        print(i)
    """

    """
    # profile the map (but not the work, which profiles as thread.lock methods)
    pool = mp.Pool(10)
    _uimap = profiled(**config)(pool.imap_unordered)
    for i in _uimap(_work, range(-10,0)):
        print(i)
    """

    """
    # profile the map, with work profiled in another thread
    pool = mp.Pool(10)
    _uimap = profiled(**config)(pool.imap_unordered)
    for i in _uimap(work, range(-10,0)):
        print(i)

    # deactivate all profiling
    disable_profiling() # in the main thread
    tuple(_uimap(disable_profiling, range(10))) # in the workers
    for i in _uimap(work, range(-20,-10)):
        print(i)
    """

    # activate profiling, but remove profiling from the worker
    enable_profiling()
    for i in map(not_profiled(work), range(-30,-20)):
        print(i)

    # print stats for profile of 'import math' in another process
    def import_ppft(*args):
        import ppft

    import pathos.pools as pp
    pool = pp.ProcessPool(1)
    profile('cumulative', pipe=pool.pipe)(import_ppft)
    pool.close()
    pool.join()
    pool.clear()


# EOF
