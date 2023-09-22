import io


def generator_for_reading_and_filtering(
    filename: str | io.TextIOBase = None,
    words: list = None
) -> str:

    def find_word(file_object: io.TextIOBase):
        for line in file_object:
            line_lst = line.lower().split()
            if words is not None:
                for word in words:
                    if word.lower() in line_lst:
                        yield line.strip()

    if isinstance(filename, str):
        with open(filename, 'r', encoding='utf-8') as file:
            for res_line in find_word(file):
                yield res_line
    elif isinstance(filename, io.TextIOBase):
        for res_line in find_word(filename):
            yield res_line
    else:
        raise TypeError("input filename or file object")
