#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2023-2026 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE

from pathos.pools import *
try:
    import numpy
    import sys
    if numpy.__version__ < '2.4.0' and sys.hexversion == 0x30f00a3:
        HASNUMPY = False #NOTE: numpy Segfaults for the above combination
    else:
        HASNUMPY = True
except ImportError:
    HASNUMPY = False


def random(x):
    from pathos.helpers import mp_helper as mp
    result = mp.random_state('random').random()
    return result + x

def rand(x):
    from pathos.helpers import mp_helper as mp
    import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        result = mp.random_state('numpy.random').rand()
    return result + x

def wrong1(x):
    import random
    result = random.random()
    return result + x

def wrong2(x):
    import numpy
    import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)
    result = numpy.random.rand()
    return result + x


def check_random(pool):
    res = pool.map(random, range(2))
    assert res[0] != res[1]
    if HASNUMPY:
        res = pool.map(rand, range(2))
        assert res[0] != res[1]
    pool.close()
    pool.join()
    pool.clear()
    return


def check_wrong(pool):
    res = pool.map(wrong1, range(2))
    assert res[0] == res[1]
    if HASNUMPY:
        res = pool.map(wrong2, range(2))
        assert res[0] == res[1]
    pool.close()
    pool.join()
    pool.clear()
    return


def test_random():
    check_random(ThreadPool())
    check_random(ProcessPool())
    check_random(ParallelPool())

def test_wrong():
    check_random(ProcessPool())
    check_random(ParallelPool())


if __name__ == '__main__':
    from pathos.helpers import freeze_support, shutdown
    freeze_support()
    test_random()
    shutdown()
