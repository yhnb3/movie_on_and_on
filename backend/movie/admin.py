from django.contrib import admin

from movie.models import Movie, Genre,MovieScore, Actor, Director
# Register your models here

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(MovieScore)
admin.site.register(Actor)
admin.site.register(Director)