import cProfile
import io
import pstats


def profile_deco(func):
    pr = cProfile.Profile()

    def wrapper(*args, **kwargs):
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        return result

    def print_stat():
        s = io.StringIO()
        sort_by = "cumulative"
        ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
        ps.print_stats()
        print(s.getvalue())

    wrapper.print_stat = print_stat

    return wrapper
