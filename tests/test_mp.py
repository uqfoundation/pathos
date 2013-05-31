# instantiate and configure the worker pool
from pathos.multiprocessing import ProcessingPool
pool = ProcessingPool(nodes=4)

_result = map(pow, [1,2,3,4], [5,6,7,8]) 

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

