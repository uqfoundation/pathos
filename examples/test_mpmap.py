#!/usr/bin/env python

from pathos.mp_map import mp_map

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())


print "Evaluate 5 items on 2 proc:"
res3 = mp_map(host, range(5), nproc=2)
print '\n'.join(res3)
print ''

print "Evaluate 5 items on 10 proc:"
res5 = mp_map(host, range(5), nproc=10) 
print '\n'.join(res5)

# end of file
