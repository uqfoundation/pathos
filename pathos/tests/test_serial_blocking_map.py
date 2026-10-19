from pathos.serial import SerialPool


def test_map_returns_a_list():
    pool = SerialPool()
    assert pool.map(abs, [-1, 2, -3]) == [1, 2, 3]
    assert isinstance(pool.map(abs, []), list)


def test_map_finishes_before_returning():
    calls = []
    result = SerialPool().map(lambda x: calls.append(x) or x * 2, [1, 2])
    assert calls == [1, 2]
    assert result == [2, 4]


def test_map_raises_before_returning():
    error = ValueError('mapping failed')

    def fail(value):
        raise error

    try:
        SerialPool().map(fail, [1])
    except ValueError as caught:
        assert caught is error
    else:
        raise AssertionError('blocking map did not raise')


def test_map_accepts_multiple_iterables():
    result = SerialPool().map(pow, iter([1, 2, 3]), [2, 3])
    assert result == [1, 8]


def test_imap_remains_lazy():
    calls = []
    result = SerialPool().imap(lambda x: calls.append(x) or x * 2, [1, 2])
    assert calls == []
    assert iter(result) is result
    assert list(result) == [2, 4]
    assert calls == [1, 2]


def test_closed_pool_rejects_map():
    pool = SerialPool()
    pool.close()
    try:
        pool.map(abs, [-1])
    except ValueError:
        pass
    else:
        raise AssertionError('closed pool accepted map')


if __name__ == '__main__':
    test_map_returns_a_list()
    test_map_finishes_before_returning()
    test_map_raises_before_returning()
    test_map_accepts_multiple_iterables()
    test_imap_remains_lazy()
    test_closed_pool_rejects_map()
