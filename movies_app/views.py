from django.shortcuts import render, redirect
from .models import Movie
from .utils import add_movie_to_db
from .utils import generate_movie


def movie_list(request):
    movies = Movie.objects.all()
    return render(request, "movies.html", {"movies": movies})


def add_movie_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        genre = request.POST.get("genre")
        year = request.POST.get("year")
        description = request.POST.get("description")

        add_movie_to_db(title, genre, year, description)

        return redirect("movie_list")

    return render(request, "add_movie.html")

def generate_movie_view(request):
    generate_movie()
    return redirect("movie_list")  # Redirect back to the movie list
