#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2021 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE

from . import pp_helper
from . import mp_helper
import ppft as parallelpython

try:
    import multiprocess as mp
    from multiprocess.pool import Pool as ProcessPool
    from multiprocess import cpu_count
    from multiprocess.dummy import Pool as ThreadPool
    from multiprocess import freeze_support
    HAS_FORK = True
except ImportError:
    HAS_FORK = False

try:
    if HAS_FORK: raise ValueError('multiprocess')

    import processing as mp
    from processing.pool import Pool as ProcessPool  # use pathos/external
    from processing import cpuCount as cpu_count
    from processing import freezeSupport as freeze_support
    try:
        import queue
    except ImportError:
        import Queue as queue

    class ThreadPool(ProcessPool):
        from processing.dummy import Process
        def __init__(self, processes=None, initializer=None, initargs=()):
            ProcessPool.__init__(self, processes, initializer, initargs)
            return
        def _setup_queues(self):
            self._inqueue = queue.Queue()
            self._outqueue = queue.Queue()
            self._quick_put = self._inqueue.put
            self._quick_get = self._outqueue.get
            return
        @staticmethod
        def _help_stuff_finish(inqueue, task_handler, size):
            # put sentinels at head of inqueue to make workers finish
            inqueue.not_empty.acquire()
            try:
                inqueue.queue.clear()
                inqueue.queue.extend([None] * size)
                inqueue.not_empty.notify_all()
            finally:
                inqueue.not_empty.release()
            return

except ImportError:  # fall-back to package distributed with python
    import multiprocessing as mp
    from multiprocessing.pool import Pool as ProcessPool
    from multiprocessing import cpu_count
    from multiprocessing.dummy import Pool as ThreadPool
    from multiprocessing import freeze_support
except ValueError: pass
del HAS_FORK

from pathos.pools import _clear as shutdown
