from django.shortcuts import render, redirect, get_object_or_404
import requests
from .models import Movie
from .utils import generate_movie, TMDB_API_KEY


def movie_list(request):
    """
    Display all movies along with any current recommended movie.
    """
    movies = Movie.objects.all()
    recommended = request.session.get("recommended_movie", None)
    return render(request, "movies.html", {"movies": movies, "recommended_movie": recommended})


def add_movie_to_list(request):
    """
    Adds the recommended movie to the database.
    It fetches detailed genre information from TMDb using the stored tmdb_id,
    and then saves the movie with up to three genres.
    Only the primary genre (first genre from TMDb) is mandatory.
    """
    recommended = request.session.get("recommended_movie", None)

    if recommended:

        tmdb_id = recommended.get("tmdb_id")

        if not tmdb_id:
            return redirect("movie_list")

        # Fetch full movie details from TMDb
        resp = requests.get(f"https://api.themoviedb.org/3/movie/{tmdb_id}",
                            params={"api_key": TMDB_API_KEY})

        if resp.status_code != 200:
            return redirect("movie_list")

        details = resp.json()
        genres = [g["name"] for g in details.get("genres", [])]
        primary_genre = genres[0] if genres else ""
        secondary_genre = genres[1] if len(genres) > 1 else ""
        third_genre = genres[2] if len(genres) > 2 else ""

        # Add the movie only if it doesn't already exist
        if not Movie.objects.filter(title=recommended["title"]).exists():
            Movie.objects.create(
                title=recommended["title"],
                primary_genre=primary_genre,
                secondary_genre=secondary_genre,
                third_genre=third_genre,
                year=recommended["year"],
                description=recommended["overview"]
            )

        # Remove recommendation from session after adding
        request.session.pop("recommended_movie", None)

    return redirect("movie_list")


def generate_movie_view(request):
    """
    View to generate a recommended movie.
    """
    generate_movie(request)
    return redirect("movie_list")


def delete_movie(request, movie_id):
    """
    Deletes a movie from the database.
    """
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return redirect("movie_list")


def edit_movie(request, movie_id):
    """
    Edit an existing movie's details.
    """
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == "POST":
        movie.title = request.POST.get("title")
        movie.primary_genre = request.POST.get("primary_genre")
        movie.secondary_genre = request.POST.get("secondary_genre") or ""
        movie.third_genre = request.POST.get("third_genre") or ""
        movie.year = int(request.POST.get("year"))
        movie.description = request.POST.get("description")
        movie.save()
        return redirect("movie_list")

    return render(request, "edit_movie.html", {"movie": movie})

def add_movie_view(request):

    """Handles adding a movie with up to three genres (only the primary is required)."""
    if request.method == "POST":
        title = request.POST["title"]
        primary_genre = request.POST["primary_genre"]
        secondary_genre = request.POST.get("secondary_genre")  # Optional
        third_genre = request.POST.get("third_genre")  # Optional
        year = int(request.POST["year"])
        description = request.POST.get("description", "")

        Movie.objects.create(
            title = title,
            primary_genre = primary_genre,
            secondary_genre = secondary_genre if secondary_genre else None,
            third_genre = third_genre if third_genre else None,
            year = year,
            description = description
        )

        return redirect("movie_list")

    return render(request, "add_movie.html")