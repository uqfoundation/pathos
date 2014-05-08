#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE

from dill import source
def test1(obj):
    _obj = source._wrap(obj)
    assert _obj(1.57) == obj(1.57)
    src = source.getimportable(obj, alias='_f')
    exec src in globals(), locals()
    assert _f(1.57) == obj(1.57)
    name = source.getname(obj)
    assert name == obj.__name__ or src.split("=",1)[0].strip()

def test2(obj):
    from pathos.pp import ParallelPythonPool
    p = ParallelPythonPool(2)
    x = [1,2,3]
    assert map(obj, x) == p.map(obj, x)


if __name__ == '__main__':

    from math import sin
    f = lambda x:x+1
    def g(x):
        return x+2

   #for func in [g, f, abs, sin]:
    for func in [g, f, sin]:
        test1(func)
        test2(func)

# EOF
