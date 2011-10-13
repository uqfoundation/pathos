#!/usr/bin/env python

from pathos.mp_map import mp_map

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())


print "Evaluate 10 items on 1 proc"
res3 = mp_map(host, range(10), nproc=1)
print '\n'.join(res3)
print ''

print "Evaluate 10 items on 2 proc"
res5 = mp_map(host, range(10), nproc=2) 
print '\n'.join(res5)
print ''

print "Evaluate 10 items on ? proc"
res7 = mp_map(host, range(10)) 
print '\n'.join(res7)
print ''

print "Evaluate 10 items on ? proc (using threads)"
res9 = mp_map(host, range(10), threads=True) 
print '\n'.join(res9)
print ''

# end of file
