import requests
from collections import Counter

from django.shortcuts import get_object_or_404, redirect, render

from movies_app.models import Movie

TMDB_API_KEY = "d357c7bb97078beca9b74338cb621a59"
TMDB_BASE_URL = "https://api.themoviedb.org/3"


def get_top_genres():
    """
    Analyze movies in the database to determine the dominant genre combination.
    Primary genres are given extra weight.
    Returns a tuple: (primary_genre, secondary_genre, third_genre).
    If a genre is missing, it returns an empty string.
    """
    movies = Movie.objects.all()

    if not movies:
        return "", "", ""

    # Count primary genres (with extra weight)
    primary_count = Counter(movie.primary_genre for movie in movies)
    primary = primary_count.most_common(1)[0][0] if primary_count else ""

    # Count secondary and third genres only from movies whose primary genre equals the chosen primary
    secondary_count = Counter()
    third_count = Counter()

    for movie in movies:
        if movie.primary_genre == primary:
            if movie.secondary_genre:
                secondary_count[movie.secondary_genre] += 1
            if movie.third_genre:
                third_count[movie.third_genre] += 1

    secondary = secondary_count.most_common(1)[0][0] if secondary_count else ""
    third = third_count.most_common(1)[0][0] if third_count else ""

    return primary, secondary, third


def get_genre_ids(genres):

    """
    Given a list of genre names, return a list of corresponding TMDb genre IDs.
    """
    response = requests.get(f"{TMDB_BASE_URL}/genre/movie/list", params={"api_key": TMDB_API_KEY})

    if response.status_code != 200:
        return []

    data = response.json().get("genres", [])

    # Create a mapping of genre names to their IDs (all lower-case)
    genre_map = {genre["name"].lower(): genre["id"] for genre in data}
    ids = [genre_map.get(g.lower()) for g in genres if g and genre_map.get(g.lower())]

    return ids


def get_best_movie(leading_genre_id, secondary_genre_id=None, third_genre_id=None):
    """
    Query TMDb to get the best-rated movie that matches the given genre IDs.
    This function enforces that the leading genre is dominant.
    """
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

    if third_genre_id:
        params["with_genres"] += f",{third_genre_id}"

    response = requests.get(f"{TMDB_BASE_URL}/discover/movie", params=params)

    if response.status_code != 200:
        return None

    movies = response.json().get("results", [])
    existing_titles = set(Movie.objects.values_list("title", flat=True))

    for movie in movies:
        # Get detailed movie info to verify genre ordering
        details_resp = requests.get(f"{TMDB_BASE_URL}/movie/{movie['id']}", params={"api_key": TMDB_API_KEY})

        if details_resp.status_code != 200:
            continue

        details = details_resp.json()
        movie_genre_ids = [g["id"] for g in details.get("genres", [])]

        if movie_genre_ids and movie_genre_ids[0] == leading_genre_id and movie["title"] not in existing_titles:
            return movie

    return None


def generate_movie(request):
    """
    Generate a recommended movie based on the user's watched movies.
    The recommendation is stored in the session.
    """
    primary, secondary, third = get_top_genres()

    if not primary:
        request.session["recommended_movie"] = None
        return

    # Get the corresponding TMDb genre IDs (ignore empty strings)
    genre_ids = get_genre_ids([g for g in [primary, secondary, third] if g])

    if not genre_ids:
        request.session["recommended_movie"] = None
        return

    recommended = get_best_movie(
        genre_ids[0],
        genre_ids[1] if len(genre_ids) > 1 else None,
        genre_ids[2] if len(genre_ids) > 2 else None
    )

    if recommended:
        poster_path = recommended.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

        # Store the TMDb ID for later genre-fetching when adding the movie
        request.session["recommended_movie"] = {
            "tmdb_id": recommended["id"],
            "title": recommended["title"],
            "year": recommended.get("release_date", "Unknown")[:4],
            "rating": recommended.get("vote_average", "N/A"),
            "tmdb_url": f"https://www.themoviedb.org/movie/{recommended['id']}",
            "overview": recommended.get("overview", "No description available."),
            "poster_url": poster_url,
            "genre": primary  # For display purposes, store only the primary genre here
        }

    else:
        request.session["recommended_movie"] = None

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
