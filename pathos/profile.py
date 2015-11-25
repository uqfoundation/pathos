#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2015 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
"""
profile: multi-thread/multi-processing capable profiling

inspired by: http://stackoverflow.com/a/32522579/4646678
"""
profiler = None

def process_id():
    from pathos.helpers import mp
    return mp.current_process().pid

def thread_id():
    import threading as th
    return th.current_thread().ident

class profiled(object):
    "decorator for profiling a function (possibly exectued in another thread)"
    def __init__(self, idgen=None, pre='id-', post='.prof'):
        "NOTE: y=idgen(), with y an indentifier (e.g. current_process().pid)"
        self.pre = pre
        self.post= post
       #self.pid = lambda : '' if idgen is None else idgen
        self.pid = process_id if idgen is None else idgen
    def __call__(self, f):
        def proactive(*args, **kwds):
            try:
                profiler.enable()
                doit = True
            except AttributeError: doit = False
            except NameError: doit = False
            res = f(*args, **kwds)
            if doit:
                profiler.disable() #XXX: option to print/get instead of dump?
                profiler.dump_stats('%s%s%s' % (self.pre,self.pid(),self.post))
            return res
        proactive.__wrapped__ = f #XXX: conflicts with other __wrapped__ ?
        return proactive

def not_profiled(f):
    "decorator to remove profiling from a function"
    if getattr(f, '__name__', None) == 'proactive':
        _f = getattr(f, '__wrapped__', f)
    else:
        _f = f
    def wrapper(*args, **kwds):
        return _f(*args, **kwds)
    return wrapper

def enable_profiling(*args): #XXX: args ignored (needed for use in map)
    "initialize (but don't start) profiling in the current thread"
    global profiler #XXX: better profiler[0] or dict?
    import cProfile
    profiler = cProfile.Profile()  #XXX: access at: pathos.profile.profiler
    return

def start_profiling(*args):
    "begin profiling everything in the current thread"
    if profiler is None: enable_profiling()
    try: profiler.enable()
    except AttributeError: pass
    except NameError: pass
    return

def stop_profiling(*args):
    "stop profiling everything in the current thread"
    try: profiler.disable()
    except AttributeError: pass
    except NameError: pass
    return

def disable_profiling(*args):
    "disable profiling in the current thread"
    if profiler is not None: stop_profiling()
    globals().pop('profiler', None)
    global profiler
    profiler = None
    return

def clear_stats(*args):
    "clear all exisiting profiling results in the current thread"
    try: profiler.clear()
    except AttributeError: pass
    except NameError: pass
    return

def get_stats(*args):
    "get all existing profiling results for the current thread"
    try: res = profiler.getstats()
    except AttributeError: pass
    except NameError: pass
    return res

def print_stats(*args, **kwds): #kwds=dict(sort=-1)
    "print all existing profiling results for the current thread"
    sort = kwds.get('sort', -1)
    try: profiler.print_stats(sort)
    except AttributeError: pass
    except NameError: pass
    return

def dump_stats(*args, **kwds): # kwds=dict(idgen=None, pre='id-', post='.prof'))
    "dump all existing profiling results for the current thread"
    config = dict(idgen=None, pre='id-', post='.prof')
    config.update(kwds)
    pre = config['pre']
    post= config['post']
    pid = config['idgen']
    pid = process_id if pid is None else pid
    file = '%s%s%s' % (pre, pid(), post)
    try: profiler.dump_stats(file)
    except AttributeError: pass
    except NameError: pass
    return

"""
def _enable_profiling(f): #FIXME: gradual: only applied to *new* workers
    "activate profiling for the given function in the current thread"
    def func(*arg, **kwd):
        enable_profiling()
        #XXX: include f under profiler or above?
        return f(*arg, **kwd)
#   func.__wrapped__ = f #XXX: conflict with other usings __wrapped__ 
    return func

def _disable_profiling(f): #FIXME: gradual: only applied to *new* workers
    "deactivate profiling for the given function in the current thread"
    try: _f = f.__wrapped__
    except AttributeError: _f = f
    def func(*arg, **kwd):
        disable_profiling()
        #XXX: include f under profiler or above?
        return _f(*arg, **kwd)
    func.__wrapped__ = _f
    return func

def profiling(pool):
    "decorator for initializing profiling functions called within a pool"
    def wrapper(*args, **kwds):
        initializer = kwds.get('initializer', None)
        pool._rinitializer = initializer
        if initializer is None: initializer = lambda *x,**y: (x,y)
        kwds['initializer'] = _enable_profiling(initializer)
        return pool(*args, **kwds)

    return wrapper
"""


# EOF
