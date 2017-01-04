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
    from pathos.helpers import freeze_support
    freeze_support()

    from pathos.pools import ProcessPool as Pool
    pool = Pool()

    print("Evaluate 5 items on 2 proc:")
    pool.ncpus = 2
    res3 = pool.map(host, range(5))
    print(pool)
    print('\n'.join(res3))
    print('')

    print("Evaluate 5 items on 10 proc:")
    pool.ncpus = 10
    res5 = pool.map(host, range(5)) 
    print(pool)
    print('\n'.join(res5))

# end of file
