from contextlib import contextmanager
from types import SimpleNamespace

import pathos.parallel as parallel
from pathos.helpers import parallelpython


class FakeServer:
    def __init__(self, ncpus='autodetect', ppservers=()):
        self.initial_ncpus = ncpus
        self.ncpus = 3 if ncpus == 'autodetect' else ncpus
        self.auto_ppservers = []
        self.ppservers = [(host, int(port))
                          for host, port in (server.split(':') for server in ppservers)]
        self._exiting = False

    def get_ncpus(self):
        return self.ncpus

    def set_ncpus(self, ncpus):
        self.ncpus = 3 if ncpus == 'autodetect' else ncpus

    def destroy(self):
        self._exiting = True


@contextmanager
def server_factory(native=False):
    original_pp, original_count = parallel.pp, parallel.cpu_count
    servers, calls = [], []

    def create(**kwds):
        requested = kwds.get('ncpus', 'autodetect')
        if native:
            # Bound the unfixed constructor instead of starting every host CPU.
            kwds.setdefault('ncpus', 3)
            server = parallelpython.Server(**kwds)
        else:
            server = FakeServer(**kwds)
        servers.append(server)
        calls.append((requested, server.get_ncpus()))
        return server

    parallel.pp = SimpleNamespace(
        Server=create, DestroyedServerError=parallelpython.DestroyedServerError)
    parallel.cpu_count = lambda: 3
    try:
        yield calls
    finally:
        for server in servers:
            server.destroy()
        state = parallel.ParallelPool.__state__
        for identifier, server in list(state.items()):
            if server in servers:
                state.pop(identifier)
        parallel.pp, parallel.cpu_count = original_pp, original_count


def check_initial_workers(nodes):
    with server_factory(native=True) as calls:
        pool = parallel.ParallelPool(nodes=nodes, id=object())
        assert pool.nodes == nodes
        assert pool._serve().get_ncpus() == nodes
        assert calls == [(nodes, nodes)]


def test_zero_local_workers():
    check_initial_workers(0)


def test_one_local_worker():
    check_initial_workers(1)


def test_two_local_workers():
    check_initial_workers(2)


def test_replacement_server_gets_worker_count():
    with server_factory() as calls:
        pool = parallel.ParallelPool(nodes=2, id=object())
        pool.servers = ('unreachable.invalid:1234',)
        assert pool._serve().get_ncpus() == 2
        assert calls == [(2, 2), (2, 2)]


def test_unspecified_workers_still_autodetect():
    with server_factory() as calls:
        pool = parallel.ParallelPool(id=object())
        assert pool.nodes == '*'
        assert pool._serve().get_ncpus() == 3
        assert calls == [('autodetect', 3)]


def test_matching_cached_server_is_reused():
    identifier = object()
    server = parallelpython.Server(ncpus=1, ppservers=())
    parallel.ParallelPool.__state__[identifier] = server
    try:
        with server_factory() as calls:
            pool = parallel.ParallelPool(nodes=1, id=identifier)
            assert pool._serve() is server
            assert calls == []
    finally:
        server.destroy()
        parallel.ParallelPool.__state__.pop(identifier, None)


if __name__ == '__main__':
    test_zero_local_workers()
    test_one_local_worker()
    test_two_local_workers()
    test_replacement_server_gets_worker_count()
    test_unspecified_workers_still_autodetect()
    test_matching_cached_server_is_reused()
