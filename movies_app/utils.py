from collections import Counter
import requests
from django.shortcuts import get_object_or_404, redirect, render

from movies_app.models import Movie

# TMDb API Configuration
TMDB_API_KEY = "d357c7bb97078beca9b74338cb621a59"
TMDB_BASE_URL = "https://api.themoviedb.org/3"


def add_movie_to_db(title, genre, year, description):
    """Creates and saves a new movie entry in the database."""
    return Movie.objects.create(
        title = title,
        genre = genre,
        year = year,
        description = description
    )

def edit_movie(request, movie_id):
    """Edits a movie's details."""
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == "POST":
        movie.title = request.POST["title"]
        movie.genre = request.POST["genre"]
        movie.year = int(request.POST["year"])
        movie.description = request.POST["description"]
        movie.save()
        return redirect("movie_list")

    return render(request, "edit_movie.html", {"movie": movie})

def delete_movie(request, movie_id):
    """Deletes a movie from the database."""
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return redirect("movie_list")

def get_top_genres():
    """Finds the most frequently watched genres from stored movies."""
    movies = Movie.objects.all()

    if not movies:
        return None, None

    genre_counter = Counter()

    for movie in movies:
        genre_counter.update(
            movie.genre.split(", ")
        )

    common_genres = genre_counter.most_common(2)
    leading_genre = common_genres[0][0] if common_genres else None
    secondary_genre = common_genres[1][0] if len(common_genres) > 1 else None

    return leading_genre, secondary_genre


def fetch_tmdb_genres():
    """Fetches the genre list from TMDb and returns a mapping of names to IDs."""
    response = requests.get(
        f"{TMDB_BASE_URL}/genre/movie/list",
        params={"api_key": TMDB_API_KEY}
    )

    if response.status_code != 200:
        return {}

    return {
        genre["name"].lower(): genre["id"]
        for genre in response.json().get(
            "genres",
            []
        )
    }


def get_genre_ids(genres):
    """Converts genre names to their corresponding TMDb IDs."""
    genre_map = fetch_tmdb_genres()
    return [
        genre_map[g.lower()]
        for g in genres if g and g.lower() in genre_map
    ]


def get_best_movie(leading_genre_id, secondary_genre_id = None):
    """Finds the highest-rated movie on TMDb with the specified genres."""
    if not leading_genre_id:
        return None

    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "sort_by": "vote_average.desc",
        "vote_count.gte": 100,
        "with_genres": str(leading_genre_id)
    }
    if secondary_genre_id:
        params["with_genres"] += f",{secondary_genre_id}"

    response = requests.get(
        f"{TMDB_BASE_URL}/discover/movie",
        params=params
    )

    if response.status_code != 200:
        return None

    movies = response.json().get(
        "results",
        [])

    existing_titles = set(Movie.objects.values_list(
        "title",
        flat=True)
    )

    for movie in movies:

        movie_details = requests.get(
            f"{TMDB_BASE_URL}/movie/{movie['id']}",
            params={"api_key": TMDB_API_KEY}
        ).json()

        movie_genres = [g["id"] for g in movie_details.get("genres", [])]

        if (movie_genres and movie_genres[0] == leading_genre_id
                and movie["title"] not in existing_titles):
            return movie

    return None


def generate_movie(request):
    """Generates a recommended movie based on top-watched genres and stores it in session."""
    leading_genre, secondary_genre = get_top_genres()
    if not leading_genre:
        request.session["recommended_movie"] = None
        return

    genre_ids = get_genre_ids(
        [leading_genre, secondary_genre]
        if secondary_genre
        else [leading_genre]
    )

    if not genre_ids:
        request.session["recommended_movie"] = None
        return

    recommended_movie = get_best_movie(
        genre_ids[0],
        genre_ids[1]
        if len(genre_ids) > 1
        else None
    )

    if recommended_movie:
        poster_path = recommended_movie.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
        movie_details = requests.get(f"{TMDB_BASE_URL}/movie/{recommended_movie['id']}",
                                     params={"api_key": TMDB_API_KEY}).json()
        genres = [g["name"] for g in movie_details.get("genres", [])]
        genre_str = ", ".join(genres) if genres else "Unknown"
        request.session["recommended_movie"] = {
            "title": recommended_movie["title"],
            "year": recommended_movie.get("release_date", "Unknown")[:4],
            "genre": genre_str,
            "rating": recommended_movie.get("vote_average", "N/A"),
            "tmdb_url": f"https://www.themoviedb.org/movie/{recommended_movie['id']}",
            "overview": recommended_movie.get("overview", "No description available."),
            "poster_url": poster_url if poster_url else None
        }
    else:
        request.session["recommended_movie"] = None
