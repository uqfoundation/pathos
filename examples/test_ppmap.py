#!/usr/bin/env python

from pathos.pp_map import pp_map
from pathos.pp_map import stats

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())


print "Evaluate 10 items on 1 cpu"
res3 = pp_map(host, range(10), ncpus=1)
print '\n'.join(res3)
print stats()
print ''

print "Evaluate 10 items on 2 cpus"
res5 = pp_map(host, range(10), ncpus=2) 
print '\n'.join(res5)
print stats()
print ''

# end of file
