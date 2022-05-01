from movies.models import Movie
from planets.models import Planet

planets = ["Tatooine", "Alderaan", "Yavin IV", "Coruscant", "Hoth"]
movies = [
    {"name": "A New Hope", "release_date": "1977-05-25"},
    {"name": "The Empire Strikes Back", "release_date": "1980-05-17"},
    {"name": "Return of the Jedi", "release_date": "1983-05-25"},
    {"name": "The Phantom Menace", "release_date": "1999-05-19"},
    {"name": "Attack of the Clones", "release_date": "2002-05-16"},
    {"name": "Revenge of the Sith", "release_date": "2005-05-19"},
]


def populate_dummy_data():
    for planet in planets:
        Planet.objects.create(name=planet)

    for movie in movies:
        Movie.objects.create(
            name=movie["name"],
            release_date=movie["release_date"]
        )
