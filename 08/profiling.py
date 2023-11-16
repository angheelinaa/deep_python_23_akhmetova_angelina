import weakref
import time
import cProfile
import io
import pstats
from memory_profiler import profile


class GeneralClass:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.value}"


class NormalClass:
    def __init__(self, obj_1, obj_2, obj_3):
        self.value_dict = {"obj_1": obj_1, "obj_2": obj_2}
        self.attr = obj_3

    def __str__(self):
        return f"normal attr: {self.attr}, normal dict: {self.value_dict}"


class SlotsClass:
    __slots__ = ("attr", "value_dict")

    def __init__(self, obj_1, obj_2, obj_3):
        self.value_dict = {"obj_1": obj_1, "obj_2": obj_2}
        self.attr = obj_3

    def __str__(self):
        return f"slot attr: {self.attr}, slot dict: {self.value_dict}"


class WeakClass:
    def __init__(self, obj_1, obj_2, obj_3):
        self.value_dict = weakref.WeakValueDictionary({"obj_1": obj_1, "obj_2": obj_2})
        self.attr = weakref.ref(obj_3) if obj_3 is not None else obj_3

    def __str__(self):
        lst_values = [value() for value in self.value_dict.valuerefs()]
        return "weak attr {}, weak dict {}".format(self.attr(),
                                                   {"obj_1": lst_values[0],
                                                    "obj_2": lst_values[1]})


def creating_objects(cls, cnt):
    start_time = time.time()
    lst_objects = [
        cls(GeneralClass(123), GeneralClass("abcd"), GeneralClass([1, 2, 3]))
        for _ in range(cnt)
    ]
    end_time = time.time()
    return lst_objects, (end_time - start_time)


def change_objects(lst_objects):
    start_time = time.time()
    for obj in lst_objects:
        obj.attr = GeneralClass(999)
        obj.value_dict = GeneralClass("qwerty")
    end_time = time.time()
    return end_time - start_time


@profile
def normal_objects(t_normal, n, cnt):
    lst_n = []
    for _ in range(n):
        lst_n, t_n = creating_objects(NormalClass, cnt)
        t_normal.append(t_n)

    for i in range(n):
        t_normal[i] = change_objects(lst_n)


@profile
def slots_objects(t_slots, n, cnt):
    lst_s = []
    for _ in range(n):
        lst_s, t_s = creating_objects(SlotsClass, cnt)
        t_slots.append(t_s)

    for i in range(n):
        t_slots[i] = change_objects(lst_s)


@profile
def weak_objects(t_weak, n, cnt):
    lst_w = []
    for _ in range(n):
        lst_w, t_w = creating_objects(WeakClass, cnt)
        t_weak.append(t_w)

    for i in range(n):
        t_weak[i] = change_objects(lst_w)


if __name__ == "__main__":
    count, N = 100000, 10
    lst_normal, lst_slots, lst_weak = [], [], []
    time_normal, time_slots, time_weak = [], [], []

    pr = cProfile.Profile()
    pr.enable()
    for i in range(N):
        lst_normal, time_n = creating_objects(NormalClass, count)
        time_normal.append(time_n)
    pr.disable()
    s = io.StringIO()
    sort_by = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
    ps.print_stats()
    print('_-' * 5, "creating objects of class with common attributes", '_-' * 5)
    print(s.getvalue())

    pr = cProfile.Profile()
    pr.enable()
    for i in range(N):
        lst_slots, time_s = creating_objects(SlotsClass, count)
        time_slots.append(time_s)
    pr.disable()
    s = io.StringIO()
    sort_by = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
    ps.print_stats()
    print('_-' * 5, "creating objects of class with slots", '_-' * 5)
    print(s.getvalue())

    pr = cProfile.Profile()
    pr.enable()
    for i in range(N):
        lst_weak, time_w = creating_objects(WeakClass, count)
        time_weak.append(time_w)
    pr.disable()
    s = io.StringIO()
    sort_by = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
    ps.print_stats()
    print('_-' * 5, "creating objects of class with weak references", '_-' * 5)
    print(s.getvalue())

    print(f"Average time of {N} iterations to create {count} objects of different classes:")
    print(f"\tclass with common attributes: {sum(time_normal) / N} seconds")
    print(f"\tclass with slots: {sum(time_slots) / N} seconds")
    print(f"\tclass with weak references: {sum(time_weak) / N} seconds")
    print('_-' * 20)

    time_normal, time_slots, time_weak = [], [], []
    pr = cProfile.Profile()
    pr.enable()
    for i in range(N):
        time_n = change_objects(lst_normal)
        time_normal.append(time_n)
    pr.disable()
    s = io.StringIO()
    sort_by = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
    ps.print_stats()
    print('_-' * 5, "changing objects of class with common attributes", '_-' * 5)
    print(s.getvalue())

    pr = cProfile.Profile()
    pr.enable()
    for i in range(N):
        time_s = change_objects(lst_slots)
        time_slots.append(time_s)
    pr.disable()
    s = io.StringIO()
    sort_by = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
    ps.print_stats()
    print('_-' * 5, "changing objects of class with slots", '_-' * 5)
    print(s.getvalue())

    pr = cProfile.Profile()
    pr.enable()
    for i in range(N):
        time_w = change_objects(lst_weak)
        time_weak.append(time_w)
    pr.disable()
    s = io.StringIO()
    sort_by = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
    ps.print_stats()
    print('_-' * 5, "changing objects of class with weak references", '_-' * 5)
    print(s.getvalue())

    print(f"Average time of {N} iterations to change {count} objects of different classes:")
    print(f"\tclass with common attributes: {sum(time_normal) / N} seconds")
    print(f"\tclass with slots: {sum(time_slots) / N} seconds")
    print(f"\tclass with weak references: {sum(time_weak) / N} seconds")

    time_normal, time_slots, time_weak = [], [], []
    normal_objects(time_normal, N, count)
    slots_objects(time_slots, N, count)
    weak_objects(time_weak, N, count)
