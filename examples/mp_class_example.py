#!/usr/bin/env python
#
# Author: Nick Rhinehart (nrhineha @cmu)
# Copyright (c) 2016 California Institute of Technology.
# Copyright (c) 2016-2021 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE

from pathos.pools import ProcessPool, ThreadPool
import logging
log = logging.getLogger(__name__)

class PMPExample(object):
    def __init__(self):
        self.cache = {}

    def compute(self, x):
        self.cache[x] = x ** 3
        return self.cache[x]

    def threadcompute(self, xs):
        pool = ThreadPool(4)
        results = pool.map(self.compute, xs)
        return results

    def processcompute(self, xs):
        pool = ProcessPool(4)
        results = pool.map(self.compute, xs)
        return results

def parcompute_example():
    dc = PMPExample()
    dc2 = PMPExample()
    dc3 = PMPExample()
    dc4 = PMPExample()

    n_datapoints = 100
    inp_data = range(n_datapoints)
    r1 = dc.threadcompute(inp_data)
    assert(len(dc.cache) == n_datapoints)

    r2 = dc2.processcompute(inp_data)
    assert(len(dc2.cache) == 0)
    assert(r1 == r2)

    r3 = ProcessPool(4).map(dc3.compute, inp_data)
    r4 = ThreadPool(4).map(dc4.compute, inp_data)
    ProcessPool.__state__.clear()
    ThreadPool.__state__.clear()
    assert(r4 == r3 == r2)
    assert(len(dc3.cache) == 0)
    assert(len(dc4.cache) == n_datapoints)

    log.info("Size of threadpooled class caches: {0}, {1}".format(len(dc.cache), len(dc4.cache)))
    log.info("Size of processpooled class caches: {0}, {1}".format(len(dc2.cache), len(dc3.cache)))

if __name__ == '__main__':
    logging.basicConfig()
    log.setLevel(logging.INFO)
    parcompute_example()
