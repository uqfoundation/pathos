import threading

import dill
from ppft import Server, _Task

from pathos.helpers.pp_helper import ApplyResult, MapResult, TimeoutError


def pending_result(as_map=False):
    task = _Task(None, 0)
    result = ApplyResult(task)
    if as_map:
        group = MapResult((1, 1))
        group.queue(result)
        result = group
    return task, result


def finish(task, value=8):
    task.finalize(dill.dumps((value, '')))


def bounded_call(result, method, timeout, complete):
    done = threading.Event()
    returned, errors = [], []

    def call():
        try:
            returned.append(getattr(result, method)(timeout))
        except BaseException as error:
            errors.append(type(error))
        finally:
            done.set()

    thread = threading.Thread(target=call)
    thread.start()
    try:
        completed = done.wait(1)
        ready = result.ready()
    finally:
        complete()
        thread.join(2)
    assert not thread.is_alive()
    assert completed, 'timed wait blocked until the task was completed'
    return returned, errors, ready


def check_get_timeout(timeout, as_map=False):
    task, result = pending_result(as_map)
    returned, errors, ready = bounded_call(
        result, 'get', timeout, lambda: finish(task))
    assert returned == []
    assert errors == [TimeoutError]
    assert not ready
    assert result.get(0) == ([8] if as_map else 8)


def test_apply_get_zero_timeout():
    check_get_timeout(0)


def test_apply_get_negative_timeout():
    check_get_timeout(-1)


def test_apply_get_positive_timeout():
    check_get_timeout(0.01)


def test_map_get_zero_timeout():
    check_get_timeout(0, as_map=True)


def check_wait_timeout(as_map=False):
    task, result = pending_result(as_map)
    returned, errors, ready = bounded_call(
        result, 'wait', 0, lambda: finish(task))
    assert returned == [None]
    assert errors == []
    assert not ready


def test_apply_wait_zero_timeout():
    check_wait_timeout()


def test_map_wait_zero_timeout():
    check_wait_timeout(as_map=True)


def test_ready_result_accepts_zero_timeout():
    task, result = pending_result()
    finish(task)
    assert result.get(0) == 8


def test_get_without_timeout_waits_for_completion():
    task, result = pending_result()
    done = threading.Event()
    values = []

    def call():
        values.append(result.get())
        done.set()

    thread = threading.Thread(target=call)
    thread.start()
    try:
        assert not done.wait(0.02)
    finally:
        finish(task)
        thread.join(2)
    assert not thread.is_alive()
    assert done.is_set()
    assert values == [8]


def test_map_shares_the_timeout_budget_across_tasks():
    first, first_result = pending_result()
    second, second_result = pending_result()
    result = MapResult((1, 2))
    result.queue(first_result, second_result)
    done, started = threading.Event(), threading.Event()
    values, errors = [], []

    def call():
        started.set()
        try:
            values.append(result.get(1))
        except BaseException as error:
            errors.append(type(error))
        finally:
            done.set()

    thread = threading.Thread(target=call)
    thread.start()
    try:
        assert started.wait(1)
        finish(first)
        assert not done.wait(0.02)
    finally:
        if not first.finished:
            finish(first)
        finish(second, 27)
        thread.join(2)
    assert not thread.is_alive()
    assert errors == []
    assert values == [[8, 27]]


def test_wait_handles_lock_release_before_finished_flag():
    task, result = pending_result()
    task.sresult = dill.dumps((8, ''))
    task.lock.release()
    done = threading.Event()
    values, errors = [], []

    def call():
        try:
            values.append(result.get(1))
        except BaseException as error:
            errors.append(type(error))
        finally:
            done.set()

    thread = threading.Thread(target=call)
    thread.start()
    try:
        assert not done.wait(0.02)
    finally:
        task.finished = True
        thread.join(2)
    assert not thread.is_alive()
    assert errors == []
    assert values == [8]


def test_native_ppft_result_honors_zero_timeout():
    entered, release = threading.Event(), threading.Event()

    def callback(value):
        entered.set()
        release.wait(10)

    server = Server(ncpus=1, ppservers=())
    try:
        task = server.submit(pow, (2, 3), callback=callback, globals={})
        assert entered.wait(5)
        result = ApplyResult(task)
        returned, errors, ready = bounded_call(result, 'get', 0, release.set)
        assert returned == []
        assert errors == [TimeoutError]
        assert not ready
        assert result.get(1) == 8
    finally:
        release.set()
        server.destroy()


if __name__ == '__main__':
    test_apply_get_zero_timeout()
    test_apply_get_negative_timeout()
    test_apply_get_positive_timeout()
    test_map_get_zero_timeout()
    test_apply_wait_zero_timeout()
    test_map_wait_zero_timeout()
    test_ready_result_accepts_zero_timeout()
    test_get_without_timeout_waits_for_completion()
    test_map_shares_the_timeout_budget_across_tasks()
    test_wait_handles_lock_release_before_finished_flag()
    test_native_ppft_result_honors_zero_timeout()
