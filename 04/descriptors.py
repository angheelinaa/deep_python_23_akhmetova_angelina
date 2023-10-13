from abc import ABC, abstractmethod
from re import sub


class BaseDescriptor(ABC):
    def __get__(self, obj, objtype):
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.name, value)

    def __set_name__(self, owner, name):
        self.name = "_" + name

    @abstractmethod
    def validate(self, value):
        pass


class NameDescriptor(BaseDescriptor):
    def __init__(self, minsize=1):
        self.minsize = minsize

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f"name '{value}' should be a str")
        if len(sub(r"[\W_]+", '', value.strip())) == 0:
            raise ValueError(f"name '{value}' should be contain alphanumeric character")
        if len(value) < self.minsize:
            raise ValueError(f"name '{value}' should be bigger than {self.minsize} or equal")


class GenreDescriptor(BaseDescriptor):
    genres = ('comedy', 'drama', 'animation', 'horror', 'science fiction',
              'adventure', 'fantasy', 'documentary', 'thriller', 'action',
              'mystery', 'western', 'historical', 'romance', 'crime')

    def validate(self, value):
        for genre in value:
            if not isinstance(genre, str):
                raise TypeError(f"genre '{genre}' should be a str")
            if genre.lower() not in GenreDescriptor.genres:
                raise ValueError(f"genre '{genre}' should be one of {GenreDescriptor.genres}")


class ReleaseYearDescriptor(BaseDescriptor):
    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError("release year should be an int")
        if value < 1870:
            raise ValueError("In fact, cinema appeared back in the 70s of the XIX century, "
                             "so input release year bigger than 1870 or equal")


class Movie:
    name = NameDescriptor()
    genres = GenreDescriptor()
    release_year = ReleaseYearDescriptor()

    def __init__(self, name, *genres, release_year):
        self.name = name
        self.genres = genres
        self.release_year = release_year

    def __str__(self):
        if self.genres:
            return f"{', '.join(self.genres)} movie {self.name}, {self.release_year}"

        return f"movie {self.name}, {self.release_year}"
