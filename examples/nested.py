#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2015-2016 California Institute of Technology.
# Copyright (c) 2016-2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE

def g(x):
  import random
  return int(x * random.random())

def h(x):
  return sum(tmap(g, x))

def f(x,y):
  return x*y

x = range(10)
y = range(5)


if __name__ == '__main__':
    from pathos.helpers import freeze_support, shutdown
    freeze_support()

    from pathos.pools import ProcessPool, ThreadPool
    amap = ProcessPool().amap
    tmap = ThreadPool().map

    print(amap(f, [h(x),h(x),h(x),h(x),h(x)], y).get())

    def _f(m, g, x, y):
      return sum(m(g,x))*y

    print(amap(_f, [tmap]*len(y), [g]*len(y), [x]*len(y), y).get())

    from math import sin, cos

    print(amap(tmap, [sin,cos], [x,x]).get())

    shutdown()

# EOF
