#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @uqfoundation)
# Copyright (c) 2024-2025 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE

from pathos.maps import Imap
from pathos.pools import ProcessPool
squared = lambda x:x*x

# serial map (in-line for loop)
print("list(map(squared, range(4))): %s" % list(map(squared, range(4))))

# pathos serial map
_map = Imap()
print("list(Imap()(squared, range(4))): %s" % list(_map(squared, range(4))))

# pathos process-parallel map
_map = Imap(ProcessPool)
print("list(Imap(ProcessPool)(squared, range(4))): %s" % list(_map(squared, range(4))))

# pathos pool-based parallel map
pool = ProcessPool()
print("list(ProcessPool().imap(squared, range(4))): %s" % list(pool.imap(squared, range(4))))

# pathos asynchronous parallel map
result = pool.amap(squared, range(4))
print("ProcessPool().amap(squared, range(4)).get(): %s" % result.get())

# pathos thread-parallel map
from pathos.pools import ThreadPool
tpool = ThreadPool()
print("list(ThreadPool().imap(squared, range(4))): %s" % list(tpool.imap(squared, range(4))))
