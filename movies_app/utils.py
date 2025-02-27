from .models import Movie

def add_movie_to_db(title, genre, year, description):
    movie = Movie.objects.create(
        title=title,
        genre=genre,
        year=year,
        description=description
    )
    return movie

def generate_movie():
    """This function will generate a movie (currently empty)"""
    print("Generating movie...")
    pass
