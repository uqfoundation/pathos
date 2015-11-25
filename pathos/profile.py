"""
multiprocessing profiler

modification of: http://stackoverflow.com/a/32522579/4646678
"""

def process_id():
    from pathos.helpers import mp
    return mp.current_process().pid

def thread_id():
    import threading as th
    return th.current_thread().ident

class profiled(object):
    "decorator for profiling a function (possibly exectued in another thread)"
    def __init__(self, idgen=None, pre='id', post='.prof'):
        "NOTE: y=idgen(), with y an indentifier (e.g. current_process().pid)"
        self.pre = pre
        self.post= post
       #self.pid = lambda : '' if idgen is None else idgen
        self.pid = process_id if idgen is None else idgen
    def __call__(self, f):
        def wrapper(*args, **kwds):
            try:
                prof.enable()
                doit = True
            except NameError:
                doit = False
            res = f(*args, **kwds)
            if doit:
                prof.disable() #XXX: option to print/get instead of dump?
                prof.dump_stats('%s%s%s' % (self.pre, self.pid(), self.post))
            return res
#       wrapper.__wrapped__ = f #XXX: conflict with other usings __wrapped__ 
        return wrapper

def start_profiling(*args): #XXX: args ignored (needed for use in map)
    "initialize (but don't enable) profiling in the current thread"
    global prof #FIXME: should be *unique* to minimize name clash (or prof[0]?)
    import cProfile
    prof = cProfile.Profile()  #XXX: access at: mprofile.prof
    return

def clear_profiling(*args):
    "clear all active profiling results in the current thread"
    try: prof.clear()
    except NameError: pass
    return

def stop_profiling(*args):
    "shutdown profiling in the current thread"
    globals().pop('prof', None)
    return

"""
def _start_profiling(f): #FIXME: gradual: only applied to *new* workers
    "activate profiling for the given function in the current thread"
    def func(*arg, **kwd):
        start_profiling()
        #XXX: include f under prof or above?
        return f(*arg, **kwd)
#   func.__wrapped__ = f #XXX: conflict with other usings __wrapped__ 
    return func

def _clear_profiling(f): #FIXME: gradual: only applied to *new* workers
    "clear profiling for the given function in the current thread"
    try: _f = f.__wrapped__
    except AttributeError: _f = f
    def func(*arg, **kwd):
        clear_profiling()
        #XXX: include f under prof or above?
        return _f(*arg, **kwd)
    func.__wrapped__ = _f
    return func

def _stop_profiling(f): #FIXME: gradual: only applied to *new* workers
    "deactivate profiling for the given function in the current thread"
    try: _f = f.__wrapped__
    except AttributeError: _f = f
    def func(*arg, **kwd):
        stop_profiling()
        #XXX: include f under prof or above?
        return _f(*arg, **kwd)
    func.__wrapped__ = _f
    return func

def profiling(pool):
    "decorator for initializing profiling functions called within a pool"
    def wrapper(*args, **kwds):
        initializer = kwds.get('initializer', None)
        pool._rinitializer = initializer
        if initializer is None: initializer = lambda *x,**y: (x,y)
        kwds['initializer'] = _start_profiling(initializer)
        return pool(*args, **kwds)

    return wrapper
"""


# EOF
