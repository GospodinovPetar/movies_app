# Create your models here.
from django.db import models

class Movie(models.Model):
    GENRE_CHOICES = [
        ("Action", "Action"),
        ("Adventure", "Adventure"),
        ("Animation", "Animation"),
        ("Comedy", "Comedy"),
        ("Crime", "Crime"),
        ("Documentary", "Documentary"),
        ("Drama", "Drama"),
        ("Family", "Family"),
        ("Fantasy", "Fantasy"),
        ("History", "History"),
        ("Horror", "Horror"),
        ("Music", "Music"),
        ("Mystery", "Mystery"),
        ("Romance", "Romance"),
        ("Science Fiction", "Science Fiction"),
        ("TV Movie", "TV Movie"),
        ("Thriller", "Thriller"),
        ("War", "War"),
        ("Western", "Western"),
    ]
    title = models.CharField(max_length=255)
    primary_genre = models.CharField(max_length=50, choices=GENRE_CHOICES)  # Required
    secondary_genre = models.CharField(max_length=50, choices=GENRE_CHOICES, blank=True, null=True)  # Optional
    third_genre = models.CharField(max_length=50, choices=GENRE_CHOICES, blank=True, null=True)  # Optional
    year = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title
