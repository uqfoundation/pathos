#!/usr/bin/env python

from pathos.pp import stats
from pathos.pp import ParallelPythonPool as Pool
pool = Pool()

def host(id):
    import socket
    import time
    time.sleep(1.0)
    return "Rank: %d -- %s" % (id, socket.gethostname())


print "Evaluate 10 items on 2 cpus" #FIXME: reset lport below
pool.ncpus = 2
pool.servers = ('localhost:5653',)
res5 = pool.map(host, range(10))
print pool
print '\n'.join(res5)
print stats()
print ''

# end of file
