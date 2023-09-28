import time
import functools


def mean(k):
    times_lst = []

    def decorator_mean(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_ts = time.time()
            result = func(*args, **kwargs)
            end_ts = time.time()
            times_lst.append(end_ts - start_ts)
            len_times_lst = len(times_lst)

            if len_times_lst > k:
                times_lst.pop(0)
                print(sum(times_lst) / k)
            else:
                print(sum(times_lst) / len_times_lst)

            return result
        return wrapper
    return decorator_mean
