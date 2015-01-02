#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2015 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE

from pathos.multiprocessing import ProcessingPool as Pool
pool = Pool()

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())


print "Evaluate 5 items on 2 proc:"
pool.ncpus = 2
res3 = pool.map(host, range(5))
print pool
print '\n'.join(res3)
print ''

print "Evaluate 5 items on 10 proc:"
pool.ncpus = 10
res5 = pool.map(host, range(5)) 
print pool
print '\n'.join(res5)

# end of file
