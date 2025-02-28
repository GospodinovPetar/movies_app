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
    genre = models.CharField(max_length=100, choices = GENRE_CHOICES) #TODO make a dropdown menu with the genres supported
    year = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title
