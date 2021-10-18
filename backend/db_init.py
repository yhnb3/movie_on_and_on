import os
import django
from django.core.management.base import BaseCommand
from backend import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'backend.settings')
django.setup()
from movie.models import Movie, Genre, MovieScore, Actor, Director
import json
import requests
import pandas as pd


genre_data = {}
with open("./data/genre_data.json", "r") as json_file:
    genre_data = json.load(json_file)

# fill genre model
genres = []
for genre in genre_data["genres"]:
    try:
        genres.append(Genre(id=genre["id"], name=genre["name"]))
    except:
        continue

Genre.objects.bulk_create(genres)


actor_data = {}
with open("./data/actors.json", "r") as json_file:
    actor_data = json.load(json_file)

actors = []
for idx, actor in enumerate(actor_data["actors"]):
    print(idx)
    try:
        actors.append(Actor(id=actor["id"], ko_name=actor["ko_name"], name=actor["name"], gender=actor["gender"], profile_path=actor["profile_path"], birthday=actor["birthday"]))
    except:
        continue

Actor.objects.bulk_create(actors, ignore_conflicts=True)

director_data = {}
with open("./data/directors.json", "r") as json_file:
    director_data = json.load(json_file)

directors = []
for idx, director in enumerate(director_data["directors"]):
    print(idx)
    try:
        directors.append(Director(id=director["id"], ko_name=director["ko_name"], name=director["name"], gender=director["gender"], profile_path=director["profile_path"], birthday=director["birthday"]))
    except:
        continue

Director.objects.bulk_create(directors, ignore_conflicts=True)



movie_data = {}
with open("./data/movie_data_final.json", "r") as json_file:
    movie_data = json.load(json_file)

for idx, movie in enumerate(movie_data["movies"]):
    if not movie["id"]:
        pass
    genres = []
    genre_string = ""
    if movie["genres"]:
        for genre in movie["genres"]:
            genres.append(genre["name"])
        genre_string = " ".join(genres)

    actors = []
    for actor in movie["actors_num"]:
        a = Actor.objects.get(id=actor).ko_name
        if a:
            actors.append(a)
        else:
            actors.append(Actor.objects.get(id=actor).name)
    actor_string = "|".join(actors)

    director_string = ""
    if movie["director_num"]:
        if Director.objects.get(id=movie["director_num"][0]).ko_name:
            director_string = Director.objects.get(id=movie["director_num"][0]).ko_name
        else:
            director_string = Director.objects.get(id=movie["director_num"][0]).name

    movie_init = Movie(title=movie["title"], actor_string=actor_string, keyword=movie["keywords"], director_string=director_string, budget=movie["budget"], overview=movie["overview"], popularity=movie["popularity"],genre_string=genre_string, id=movie["id"],
                        poster_path=movie["poster_path"], release_date=movie["release_date"], revenue=movie["revenue"], runtime=movie["runtime"], spoken_language=movie["spoken_languages"], tagline=movie["tagline"], vote_average=movie["vote_average"], vote_count=movie["vote_count"])
    print(idx)
    movie_init.save()
    for genre in movie["genres"]:
        g = Genre.objects.get(id=genre["id"])
        movie_init.genre.add(g)

    for actor in movie["actors_num"]:
        a = Actor.objects.get(id=actor)
        movie_init.actor.add(a)

    for director in movie["director_num"]:
        d = Director.objects.get(id=director)
        movie_init.director.add(d)


movies = pd.read_csv('./data/ratings_small.csv')
links_small = pd.read_csv('./data/links_small.csv')
links_small = links_small[links_small['tmdbId'].notnull()]
new_link = movies.merge(links_small, on='movieId')
new_link = new_link[["userId", "movieId","rating", "tmdbId"]].sort_values("userId").reset_index()
new_link = new_link[["userId","rating", "tmdbId"]]
new_link["tmdbId"] = new_link["tmdbId"].apply(lambda x : int(x))


movie_score = []
for i, row in new_link.iterrows():
    movie_score.append(MovieScore(user=-row["userId"], movie=row["tmdbId"], rating=row["rating"]))
MovieScore.objects.bulk_create(movie_score)


