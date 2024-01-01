#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2024 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE

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

    tpool.clear()

# end of file
