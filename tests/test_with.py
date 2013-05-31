from __future__ import with_statement
#import math   # some maps can't handle globals

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]

def is_prime(n):
    if n % 2 == 0:
        return False

    import math
    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def sleep_add1(x):
    from time import sleep
    if x < 4: sleep(x)
    return x+1

def sleep_add2(x):
    from time import sleep
    if x < 4: sleep(x)
    return x+2


if __name__ == '__main__':
   #from pathos.multiprocessing import ProcessingPool as Pool
    from pathos.pp import ParallelPythonPool as Pool

    inputs = range(10)
    with Pool() as pool1:
        res1 = pool1.amap(sleep_add1, inputs)
    with Pool() as pool2:
        res2 = pool2.amap(sleep_add2, inputs)

    from itertools import izip
    with Pool() as pool3:
        for number, prime in izip(PRIMES, pool3.imap(is_prime, PRIMES)):
            print ('%d is prime: %s' % (number, prime))

    assert res1.get() == [i+1 for i in inputs]
    assert res2.get() == [i+2 for i in inputs]


# EOF
