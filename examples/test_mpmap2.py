#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE

def host(id):
    import socket
    return "Rank: %d -- %s" % (id, socket.gethostname())


if __name__ == '__main__':
    from pathos.pools import ThreadPool as TPool
    tpool = TPool()

    print("Evaluate 10 items on 1 thread")
    tpool.nthreads = 1
    res3 = tpool.map(host, range(10))
    print(tpool)
    print('\n'.join(res3))
    print('')

    print("Evaluate 10 items on 2 threads")
    tpool.nthreads = 2
    res5 = tpool.map(host, range(10))
    print(tpool)
    print('\n'.join(res5))
    print('')

    print("Evaluate 10 items on ? threads")
    tpool.nthreads = None
    res9 = tpool.map(host, range(10)) 
    print(tpool)
    print('\n'.join(res9))
    print('')

# end of file
