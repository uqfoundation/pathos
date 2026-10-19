from contextlib import contextmanager

from pathos.parallel import ParallelPool
from pathos.helpers import parallelpython


@contextmanager
def local_pool():
    # Seed one local worker so these tests do not depend on CPU autodetection.
    server = parallelpython.Server(ncpus=1, ppservers=())
    identifier = object()
    ParallelPool.__state__[identifier] = server
    try:
        yield ParallelPool(nodes=1, id=identifier)
    finally:
        server.destroy()
        ParallelPool.__state__.pop(identifier, None)


def test_amap_accepts_a_generator():
    with local_pool() as pool:
        result = pool.amap(pow, (x for x in [1, 2, 3]), [2, 2, 2])
        assert result.get(timeout=5) == [1, 4, 9]


def test_amap_accepts_multiple_single_pass_inputs():
    calls = []

    def values():
        for value in [1, 2, 3]:
            calls.append(value)
            yield value

    with local_pool() as pool:
        result = pool.amap(pow, values(), iter([2, 3, 2]))
        assert result.get(timeout=5) == [1, 8, 9]
    assert calls == [1, 2, 3]


def test_amap_stops_at_the_shortest_input():
    with local_pool() as pool:
        result = pool.amap(pow, (x for x in [1, 2, 3]), iter([2, 3]))
        assert result.get(timeout=5) == [1, 8]


def test_amap_accepts_empty_generators():
    with local_pool() as pool:
        result = pool.amap(pow, (x for x in []), iter([2]))
        assert result.ready()
        assert result.get(timeout=0) == []


def test_amap_preserves_sized_input_results():
    with local_pool() as pool:
        assert pool.amap(pow, [1, 2, 3], [2, 3, 2]).get(timeout=5) == [1, 8, 9]


def test_amap_preserves_empty_list_results():
    with local_pool() as pool:
        result = pool.amap(pow, [], [2])
        assert result.ready()
        assert result.get(timeout=0) == []


if __name__ == '__main__':
    test_amap_accepts_a_generator()
    test_amap_accepts_multiple_single_pass_inputs()
    test_amap_stops_at_the_shortest_input()
    test_amap_accepts_empty_generators()
    test_amap_preserves_sized_input_results()
    test_amap_preserves_empty_list_results()
