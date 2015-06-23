from pathos.pools import ProcessPool, ThreadPool
amap = ProcessPool().amap
tmap = ThreadPool().map

def g(x):
  import random
  return int(x * random.random())

def h(x):
  return sum(tmap(g, x))

def f(x,y):
  return x*y

x = range(10)
y = range(5)

print amap(f, [h(x),h(x),h(x),h(x),h(x)], y).get()

def _f(m, g, x, y):
  return sum(m(g,x))*y

print amap(_f, [tmap]*len(y), [g]*len(y), [x]*len(y), y).get()

from math import sin, cos

print amap(tmap, [sin,cos], [range(10),range(10)]).get()


