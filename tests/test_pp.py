
from dill import source
def test1(obj):
    _obj = source._wrap(obj)
    assert _obj(1.57) == obj(1.57)
    src = source.getsource(obj, alias='_f')
    exec src in globals(), locals()
    assert _f(1.57) == obj(1.57)
    name = source._get_name(obj)
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

    for func in [g, f, abs, sin]:
        test1(func)
        test2(func)

# EOF
