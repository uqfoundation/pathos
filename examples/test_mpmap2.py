#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE

from pathos.multiprocessing import ProcessingPool as Pool
from pathos.multiprocessing import ThreadingPool as TPool
pool = Pool()
tpool = TPool()

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())


print "Evaluate 10 items on 1 proc"
pool.ncpus = 1
res3 = pool.map(host, range(10))
print pool
print '\n'.join(res3)
print ''

print "Evaluate 10 items on 2 proc"
pool.ncpus = 2
res5 = pool.map(host, range(10))
print pool
print '\n'.join(res5)
print ''

print "Evaluate 10 items on ? proc"
pool.ncpus = None
res7 = pool.map(host, range(10)) 
print pool
print '\n'.join(res7)
print ''

print "Evaluate 10 items on ? proc (using threads)"
tpool.nthreads = None
res9 = tpool.map(host, range(10)) 
print tpool
print '\n'.join(res9)
print ''

# end of file
