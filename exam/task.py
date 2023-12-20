'''
Напишите генератор gen_from_list на Python, который:

1. принимает список и шаг step в качестве аргументов;
2. генерирует значения из списка с первого элемента с шагом step;
3. позволяет изменить шаг на произвольной итерации через send(new_step);
4. возвращает через return общее число сгенерированных значений.

gen = gen_from_list([1, 2, 3, 4, 5, 6, 7, 8, 9], 1)

assert next(gen) == 1
assert next(gen) == 2
assert gen.send(3) == 5
assert next(gen) == 8
assert gen.send(1) == 9

next(gen) # StopIteration
'''


def gen_from_list(nums, step):
    count = 0
    i = 0
    while i < len(nums):
        new_step = yield nums[i]
        if new_step is not None:
            step = new_step
        i += step
        count += 1
    return count


'''
Написать функцию, которая принимает на вход имя файла и k - количество новых файлов.
Функция создает k новых файлов с каким-то шаблонным именем (можно также параметром функции) и 
записывает в каждый новый файл по очереди строки исходного файла.
То есть если k == 2, то все четные строки исходного файла запишутся в один новый файл, а все нечетные - 
в другой.
Запись каждого нового файла должна проводиться в отдельном потоке
'''

import threading
from typing import Generator


def gen_line(filename: str, line_num: int, k: int) -> Generator:
    with open(filename, "r") as file:
        for i, line in enumerate(file):
            if i % k == line_num:
                yield line


def create_file(gen: Generator) -> None:
    with open(threading.current_thread().name, "a") as file:
        for line in gen:
            file.write(line)


def run(filename: str, k: int, template: str) -> None:
    generators = [gen_line(filename, i, k) for i in range(k)]

    threads = [
        threading.Thread(target=create_file, name=f"{template}_{i}.txt", args=(generators[i],))
        for i in range(k)
    ]

    for th in threads:
        th.start()

    for th in threads:
        th.join()


if __name__ == "__main__":
    run("filetext.txt", 4, "output")
