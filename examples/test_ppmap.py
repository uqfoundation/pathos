#!/usr/bin/env python

from pathos.pp import stats
from pathos.pp import ParallelPythonPool as Pool
pool = Pool()

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())


print "Evaluate 10 items on 1 cpu"
pool.ncpus = 1
res3 = pool.map(host, range(10))
print pool
print '\n'.join(res3)
print stats()

print "Evaluate 10 items on 2 cpus"
pool.ncpus = 2
res5 = pool.map(host, range(10)) 
print pool
print '\n'.join(res5)
print stats()

# end of file
