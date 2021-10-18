from rest_framework import serializers
from .models import Movie, MovieScore, Actor, Director


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class MovieScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieScore
        fields = '__all__'

class ActorSerializer(serializers.ModelSerializer):
    actor_movies = MovieSerializer(many=True, read_only=True)
    class Meta:
        model = Actor
        fields = ('id', 'ko_name', 'name', 'gender', 'profile_path', 'birthday', 'actor_movies')

class ActorSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

class DirectorSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

class DirectorSerializer(serializers.ModelSerializer):
    director_movies = MovieSerializer(many=True, read_only=True)
    class Meta:
        model = Director
        fields = ('id', 'ko_name', 'name', 'gender', 'profile_path', 'birthday', 'director_movies')