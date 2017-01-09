#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE

def test_mp():
    # instantiate and configure the worker pool
    from pathos.pools import ProcessPool
    pool = ProcessPool(nodes=4)

    _result = list(map(pow, [1,2,3,4], [5,6,7,8])) 

    # do a blocking map on the chosen function
    result = pool.map(pow, [1,2,3,4], [5,6,7,8])
    assert result == _result

    # do a non-blocking map, then extract the result from the iterator
    result_iter = pool.imap(pow, [1,2,3,4], [5,6,7,8])
    result = list(result_iter)
    assert result == _result

    # do an asynchronous map, then get the results
    result_queue = pool.amap(pow, [1,2,3,4], [5,6,7,8])
    result = result_queue.get()
    assert result == _result


if __name__ == '__main__':
    from pathos.helpers import freeze_support
    freeze_support()
    test_mp()
