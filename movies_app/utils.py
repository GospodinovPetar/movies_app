import requests
from collections import Counter

from django.shortcuts import get_object_or_404, redirect, render

from movies_app.models import Movie

TMDB_API_KEY = "ee2f41a532d22c126235419787ea5f9c"
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
    Attempts to find the best-rated movie from TMDb using a three-tier fallback:
      1) Triple match: All three genres are present, and the movie's first genre equals the leading genre.
      2) Double match: Leading and secondary genres are present (ignoring order).
      3) Single match: Leading genre is present.
    Returns the first valid match, or None if nothing is found.
    """
    if not leading_genre_id:
        return None

    # Helper: searches TMDb given a list of required genre IDs.
    def discover_movies(required_ids):
        # Build the 'with_genres' parameter (e.g. "28,35,878")
        with_genres_str = ",".join(str(g) for g in required_ids)
        params = {
            "api_key": TMDB_API_KEY,
            "language": "en-US",
            "sort_by": "vote_average.desc",
            "vote_count.gte": 100,
            "with_genres": with_genres_str
        }
        response = requests.get(f"{TMDB_BASE_URL}/discover/movie", params=params)
        if response.status_code != 200:
            return None
        movies = response.json().get("results", [])
        existing_titles = set(Movie.objects.values_list("title", flat=True))
        strict_candidate = None  # relaxed candidate

        for movie in movies:
            # Fetch full details to get the movie's genre list (as IDs)
            details_resp = requests.get(f"{TMDB_BASE_URL}/movie/{movie['id']}",
                                        params={"api_key": TMDB_API_KEY})
            if details_resp.status_code != 200:
                continue
            details = details_resp.json()
            movie_genres = [g["id"] for g in details.get("genres", [])]
            # Strict check: first genre must equal the leading desired genre and all required are present
            if movie_genres and movie_genres[0] == required_ids[0] and set(required_ids).issubset(movie_genres):
                if movie["title"] not in existing_titles:
                    return movie
            # Otherwise, if the relaxed check passes (all required present regardless of order)
            if set(required_ids).issubset(movie_genres) and movie["title"] not in existing_titles:
                if strict_candidate is None:
                    strict_candidate = movie
        return strict_candidate

    # 1) Try triple: leading, secondary, third (if available)
    if secondary_genre_id and third_genre_id:
        triple_ids = [leading_genre_id, secondary_genre_id, third_genre_id]
        movie = discover_movies(triple_ids)
        if movie:
            return movie

    # 2) Fallback: Try double: leading + secondary (if available)
    if secondary_genre_id:
        double_ids = [leading_genre_id, secondary_genre_id]
        movie = discover_movies(double_ids)
        if movie:
            return movie

    # 3) Fallback: Try single: leading only
    single_ids = [leading_genre_id]
    return discover_movies(single_ids)


def generate_movie(request):
    """
    Generates a recommended movie based on the user's movie collection.
    If the database is empty, sets an error message instead.
    """
    # Check if there are any movies in the database
    from .models import Movie  # Ensure we have access to Movie model here
    if not Movie.objects.exists():
        request.session["recommended_movie"] = None
        request.session["recommendation_error"] = (
            "Sorry, I can't generate a movie without prior knowledge of your movie taste."
        )
        return

    # Clear any previous error message
    request.session.pop("recommendation_error", None)

    # Get the dominant genre combination from the entire DB
    primary, secondary, third = get_top_genres()
    if not primary:
        request.session["recommended_movie"] = None
        request.session["recommendation_error"] = (
            "Sorry, I can't generate a movie without prior knowledge of your movie taste."
        )
        return

    # Convert non-empty genre names to TMDb IDs
    desired_genres = [g for g in [primary, secondary, third] if g]
    genre_ids = get_genre_ids(desired_genres)
    if not genre_ids:
        request.session["recommended_movie"] = None
        return

    # Assign IDs: primary is mandatory, secondary and third if available
    primary_id = genre_ids[0]
    secondary_id = genre_ids[1] if len(genre_ids) > 1 else None
    third_id = genre_ids[2] if len(genre_ids) > 2 else None

    candidate = get_best_movie(primary_id, secondary_id, third_id)
    if candidate:
        poster_path = candidate.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""
        request.session["recommended_movie"] = {
            "tmdb_id": candidate["id"],
            "title": candidate["title"],
            "year": candidate.get("release_date", "Unknown")[:4],
            "rating": candidate.get("vote_average", "N/A"),
            "tmdb_url": f"https://www.themoviedb.org/movie/{candidate['id']}",
            "overview": candidate.get("overview", "No description available."),
            "poster_url": poster_url,
            "genre": primary  # for display purposes, show only the primary genre
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

def delete_movie(request, movie_id):
    """Deletes a movie from the database."""
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return redirect("movie_list")
