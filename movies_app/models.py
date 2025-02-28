# Create your models here.
from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100) #TODO make a dropdown menu with the genres supported
    year = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title
