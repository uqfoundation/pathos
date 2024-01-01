#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2024 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE

from pathos.parallel import stats
from pathos.parallel import ParallelPool as Pool
pool = Pool()

def host(id):
    import socket
    import time
    time.sleep(1.0)
    return "Rank: %d -- %s" % (id, socket.gethostname())


print("Evaluate 10 items on 2 cpus") #FIXME: reset lport below
pool.ncpus = 2
pool.servers = ('localhost:5653',)
res5 = pool.map(host, range(10))
print(pool)
print('\n'.join(res5))
print(stats())
print('')

pool.clear()

# end of file
