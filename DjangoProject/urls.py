from django.urls import path
from django.contrib import admin
from django.urls import path
from movies_app.views import add_movie_view, movie_list, generate_movie_view, add_movie_to_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", movie_list, name="movie_list"),
    path("add_movie/", add_movie_view, name="add_movie"),
    path("generate_movie/", generate_movie_view, name="generate_movie"),
    path("add_movie_to_list/", add_movie_to_list, name="add_movie_to_list"),
]
