import numpy as np
from time import time

time_arr = []


def timer_decorator(func):
    def wrapper(*args, **kwargs):
        repetitions = args[0]
        for i in range(repetitions):
            t1 = time()
            func(*args, **kwargs)
            t2 = time()
            time_arr.append((t2 - t1))
        print(f'Function {func.__name__!r} executed in {np.mean(time_arr):.8f}s +/- {np.std(time_arr):.8f}s')

    return wrapper


@timer_decorator
def testowa_funkcja(n):
    np.ones((10000, 10000))


testowa_funkcja(100)
