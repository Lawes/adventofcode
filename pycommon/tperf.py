import time
from functools import wraps
import contextlib


@contextlib.contextmanager
def context_timeperf(name=None):
    tick = time.perf_counter()
    yield tick
    dt = time.perf_counter() - tick
    name = name or 'tock'
    print(f'[{name}] : {dt:.4f} s')


def timeperf(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with context_timeperf(wrapper.__name__):
            res = func(*args, **kwargs)
        return res
    return wrapper
