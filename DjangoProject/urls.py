from django.urls import path

from movies_app.utils import generate_movie
from movies_app.views import add_movie_view, movie_list, generate_movie_view

urlpatterns = [
    path("", movie_list, name="movie_list"),
    path("add_movie/", add_movie_view, name="add_movie"),
    path("generate_movie/", generate_movie_view, name="generate_movie"),
]
