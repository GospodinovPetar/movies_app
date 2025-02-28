from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "primary_genre", "secondary_genre", "third_genre","year")  # Show these columns in the admin list view
    search_fields = ("title", "primary_genre", "secondary_genre", "third_genre")  # Enable search by title and genre
    list_filter = ("primary_genre", "secondary_genre", "third_genre", "year")  # Add filters for better navigation
    ordering = ("year",)  # Default sorting by year
