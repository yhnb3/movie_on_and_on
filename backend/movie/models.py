from django.db import models
import json
# Create your models here.


class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

class Actor(models.Model):
    id = models.IntegerField(primary_key=True)
    ko_name = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    gender = models.IntegerField()
    profile_path = models.CharField(max_length=255, null=True)
    birthday = models.CharField(max_length=30, null=True)

class Director(models.Model):
    id = models.IntegerField(primary_key=True)
    ko_name = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    gender = models.IntegerField()
    profile_path = models.CharField(max_length=255, null=True)
    birthday = models.CharField(max_length=30, null=True)


class Movie(models.Model):
    genre = models.ManyToManyField(Genre, related_name="genre_movies", null=True)
    genre_string = models.CharField(max_length=255)
    id = models.IntegerField(primary_key=True)

    actor = models.ManyToManyField(Actor, related_name="actor_movies", null=True)
    director = models.ManyToManyField(Director, related_name="director_movies", null=True)
    keyword = models.CharField(max_length=255)
    actor_string = models.CharField(max_length=255)
    director_string = models.CharField(max_length=30)
    budget = models.FloatField(null=True)
    overview = models.TextField(null=True)
    popularity = models.FloatField(null=True)
    poster_path = models.TextField(null=True)

    release_date = models.CharField(max_length=30)
    revenue = models.FloatField(null=True)
    runtime = models.FloatField(null=True)
    spoken_language = models.CharField(max_length=30)
    tagline = models.TextField(null=True)
    title = models.TextField(null=True)
    vote_average = models.FloatField(null=True)
    vote_count = models.IntegerField(null=True)

class MovieScore(models.Model):
    user = models.IntegerField()
    movie = models.IntegerField()
    rating = models.FloatField()



