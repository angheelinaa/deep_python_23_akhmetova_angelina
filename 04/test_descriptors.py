import unittest
from descriptors import NameDescriptor, GenreDescriptor, ReleaseYearDescriptor, Movie


class TestDescriptors(unittest.TestCase):
    def test_descriptors_simple(self):
        movie_1 = Movie("Knives Out", "comedy", "drama", "crime", release_year=2019)
        movie_2 = Movie("Back to the future", release_year=1985)

        self.assertIsInstance(Movie.name, NameDescriptor)
        self.assertIsInstance(Movie.genres, GenreDescriptor)
        self.assertIsInstance(Movie.release_year, ReleaseYearDescriptor)

        self.assertEqual("Knives Out", movie_1.name)
        self.assertEqual(("comedy", "drama", "crime"), movie_1.genres)
        self.assertEqual(2019, movie_1.release_year)

        self.assertEqual("Back to the future", movie_2.name)
        self.assertEqual((), movie_2.genres)
        self.assertEqual(1985, movie_2.release_year)

    def test_str(self):
        movie_1 = Movie("Knives Out", "comedy", "drama", "crime", release_year=2019)
        movie_2 = Movie("Back to the future", release_year=1985)

        self.assertEqual("comedy, drama, crime movie Knives Out, 2019", str(movie_1))
        self.assertEqual("movie Back to the future, 1985", str(movie_2))

    def test_name_descriptor(self):
        movie_1 = Movie("1+1", release_year=2023)
        self.assertEqual("1+1", movie_1.name)

        Movie.name.minsize = 3
        movie_2 = Movie("Оно", release_year=2023)
        self.assertEqual("Оно", movie_2.name)

    def test_name_descriptor_errors(self):
        with self.assertRaises(TypeError) as err:
            Movie(123, release_year=2023)
        self.assertEqual("name '123' should be a str", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            Movie(["Knives Out"], release_year=2023)
        self.assertEqual("name '['Knives Out']' should be a str", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            Movie("", release_year=2023)
        self.assertEqual("name '' should be contain alphanumeric character", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            Movie("  +!", release_year=2023)
        self.assertEqual("name '  +!' should be contain alphanumeric character", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))

        Movie.name.minsize = 3
        with self.assertRaises(ValueError) as err:
            Movie("It", release_year=2023)
        self.assertEqual("name 'It' should be bigger than 3 or equal", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))

    def test_genre_descriptor(self):
        movie_1 = Movie("Knives Out", "Drama", release_year=2019)
        self.assertEqual(("Drama",), movie_1.genres)

        movie_2 = Movie("Knives Out", "CRIME", release_year=2019)
        self.assertEqual(("CRIME",), movie_2.genres)

    def test_genre_descriptor_errors(self):
        with self.assertRaises(TypeError) as err:
            Movie("Knives Out", 123, release_year=2023)
        self.assertEqual("genre '123' should be a str", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            Movie("Knives Out", ["comedy"], release_year=2023)
        self.assertEqual("genre '['comedy']' should be a str", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            Movie("Knives Out", "comedy", 123, release_year=2023)
        self.assertEqual("genre '123' should be a str", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            Movie("Knives Out", "anime", release_year=2023)
        self.assertEqual("genre 'anime' should be one of ('comedy', 'drama', 'animation',"
                         " 'horror', 'science fiction', 'adventure', 'fantasy', 'documentary',"
                         " 'thriller', 'action', 'mystery', 'western', 'historical', 'romance',"
                         " 'crime')", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            Movie("Knives Out", "drama", "cartoon", release_year=2023)
        self.assertEqual("genre 'cartoon' should be one of ('comedy', 'drama', 'animation',"
                         " 'horror', 'science fiction', 'adventure', 'fantasy', 'documentary',"
                         " 'thriller', 'action', 'mystery', 'western', 'historical', 'romance',"
                         " 'crime')", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))

    def test_release_year_descriptor(self):
        movie_1 = Movie("Knives Out", release_year=1870)
        self.assertEqual(1870, movie_1.release_year)

        with self.assertRaises(TypeError) as err:
            Movie("Knives Out", release_year="2023")
        self.assertEqual("release year should be an int", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            Movie("Knives Out", release_year=998)
        self.assertEqual("In fact, cinema appeared back in the 70s of the XIX century,"
                         " so input release year bigger than 1870 or equal", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))

    def test_set_descriptor(self):
        movie = Movie("Knives Out", "comedy", "drama", "crime", release_year=2019)

        self.assertEqual("Knives Out", movie.name)
        movie.name = "new_name"
        self.assertEqual("new_name", movie.name)
        with self.assertRaises(TypeError):
            movie.name = 123
        with self.assertRaises(ValueError):
            movie.name = ""
        self.assertEqual("new_name", movie.name)

        self.assertEqual(("comedy", "drama", "crime"), movie.genres)
        movie.genres = ("fantasy",)
        self.assertEqual(("fantasy",), movie.genres)
        with self.assertRaises(TypeError):
            movie.genres = (123,)
        with self.assertRaises(ValueError):
            movie.genres = ("anime", )
        self.assertEqual(("fantasy",), movie.genres)

        self.assertEqual(2019, movie.release_year)
        movie.release_year = 2005
        self.assertEqual(2005, movie.release_year)
        with self.assertRaises(TypeError):
            movie.release_year = "2005"
        with self.assertRaises(ValueError):
            movie.release_year = 1700
        self.assertEqual(2005, movie.release_year)
