from django.shortcuts import render, redirect
from .models import Movie
from .utils import add_movie_to_db
from .utils import generate_movie

def movie_list(request):
    """Displays the list of movies and the generated recommendation."""
    movies = Movie.objects.all()
    recommended_movie = request.session.get("recommended_movie", None)
    return render(request, "movies.html", {"movies": movies, "recommended_movie": recommended_movie})

def generate_movie_view(request):
    generate_movie(request)
    return redirect("movie_list")

def add_movie_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        genre = request.POST.get("genre")
        year = request.POST.get("year")
        description = request.POST.get("description")

        add_movie_to_db(title, genre, year, description)

        return redirect("movie_list")

    return render(request, "add_movie.html")

def add_movie_to_list(request):
    recommended_movie = request.session.get("recommended_movie", None)

    if recommended_movie:
        # Ensure the movie isn't already in the database
        if not Movie.objects.filter(title=recommended_movie["title"]).exists():
            Movie.objects.create(
                title = recommended_movie["title"],
                genre = "Unknown",  # TMDb API doesn't provide genre names directly
                year = recommended_movie["year"],
                description = recommended_movie["overview"]
            )
            print(f"Movie '{recommended_movie['title']}' added to the database.")

        # Clear the recommended movie from the session
        request.session.pop("recommended_movie", None)

    return redirect("movie_list")