#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE
"""
Calculate the sum of all primes below given integer n.

Usage: python sum_primesX.py [tunnelport]
    [tunnelport] - the port number(s) of the local ssh tunnel connection,
    if omitted no tunneling will be used.

To establish a ssh-tunneled server, please see
    $ pathos_connect --help
"""

import math
import sys
import ppft

LOCAL_WORKERS = 'autodetect' #XXX: 'autodetect' or 0,1,2,...

def isprime(n):
    """Returns True if n is prime and False otherwise"""
    if not isinstance(n, int):
        raise TypeError("argument passed to is_prime is not of 'int' type")
    if n < 2:
        return False
    if n == 2:
        return True
    max = int(math.ceil(math.sqrt(n)))
    i = 2
    while i <= max:
        if n % i == 0:
            return False
        i += 1
    return True

def sum_primes(n):
    """Calculates sum of all primes below given integer n"""
    return sum([x for x in range(2, n) if isprime(x)])

########################################################################

print("""Usage: python sum_primesX.py [tunnelport]
    [tunnelport] - the port number(s) of the local ssh tunnel connection,
    if omitted no tunneling will be used.""")

ppservers = []
for i in range(1,len(sys.argv)):
    tunnelport = int(sys.argv[i])
    ppservers.append("localhost:%s" % tunnelport)
ppservers = tuple(ppservers)

# Creates jobserver with automatically detected number of workers
job_server = ppft.Server(ppservers=ppservers)

# Allow running without local workers
if LOCAL_WORKERS != 'autodetect':
    job_server.set_ncpus(LOCAL_WORKERS)

#print("Known servers: [('local',)] %s %s" % (job_server.ppservers,job_server.auto_ppservers))
print("Known servers: [('local',)] %s" % (job_server.ppservers))
print("Starting ppft with %s local workers" % job_server.get_ncpus())

# Submit a job of calulating sum_primes(100) for execution.
# sum_primes - the function
# (100,) - tuple with arguments for sum_primes
# (isprime,) - tuple with functions on which function sum_primes depends
# ("math",) - tuple with module names which must be imported before
#             sum_primes execution
# Execution starts as soon as one of the workers will become available
###job1 = job_server.submit(sum_primes, (100, ), (isprime, ), ("math", ))

# Retrieves the result calculated by job1
# The value of job1() is the same as sum_primes(100)
# If the job has not been finished yet, execution will
# wait here until result is available
###result = job1()

###print("Sum of primes below 100 is %s" % result)


# The following submits 8 jobs and then retrieves the results
inputs = (100000, 100100, 100200, 100300, 100400, 100500, 100600, 100700)
jobs = [(input, job_server.submit(sum_primes, (input, ), (isprime, ),
        ("math", ))) for input in inputs]

for input, job in jobs:
    print("Sum of primes below %s is %s" % (input, job()))

job_server.print_stats()

# Parallel Python Software: http://www.parallelpython.com
