#!/usr/bin/env python
"""
map helper functions
"""

def starargs(f):
    """decorator to convert a many-arg function to a single-arg function"""
    func = lambda args: f(*args)
   #func.__module__ = f.__module__
   #func.__name__ = f.__name__
    doc = "\nNOTE: all inputs have been compressed into a single argument"
    if f.__doc__: func.__doc__ = f.__doc__ + doc
    return func
   #from functools import update_wrapper
   #return update_wrapper(func, f)

