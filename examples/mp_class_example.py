from pathos.multiprocessing import ProcessingPool, ThreadingPool
import pathos.multiprocessing
import logging
log = logging.getLogger(__name__)

class PMPExample(object):
    def __init__(self):
        self.cache = {}

    def compute(self, x):
        self.cache[x] = x ** 3
        return self.cache[x]

    def threadcompute(self, xs):
        pool = ThreadingPool(4)
        results = pool.map(self.compute, xs)
        return results

    def processcompute(self, xs):
        pool = ProcessingPool(4)
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

    r3 = ProcessingPool(4).map(dc3.compute, inp_data)
    r4 = ThreadingPool(4).map(dc4.compute, inp_data)
    assert(r4 == r3 == r2)
    assert(len(dc3.cache) == 0)
    assert(len(dc4.cache) == n_datapoints)

    log.info("Size of threadpooled class caches: {}, {}".format(len(dc.cache), len(dc4.cache)))
    log.info("Size of processpooled class caches: {}, {}".format(len(dc2.cache), len(dc3.cache)))

if __name__ == '__main__':
    logging.basicConfig()
    log.setLevel(logging.INFO)
    parcompute_example()
