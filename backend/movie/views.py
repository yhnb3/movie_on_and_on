from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import get_user_model

from .models import Movie, Genre, MovieScore, Actor, Director
from .serializers import MovieSerializer, MovieScoreSerializer, ActorSerializer, DirectorSerializer, ActorSearchSerializer, DirectorSearchSerializer
from search.models import Search
from search.serializers import SearchSerializer

from django.db.models import Q

## 추천
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from surprise import Reader, Dataset, SVD
from surprise import accuracy
from surprise.model_selection import cross_validate
from surprise.model_selection import train_test_split


import warnings; warnings.simplefilter('ignore')
import json
import joblib
from datetime import datetime

user = get_user_model()

error_message = "error"

class MovieView(APIView):
    def get(self, request, **kwargs):
        if kwargs.get('id') is None:
            movies = Movie.objects.all().order_by('-vote_count')[:100]
            serializer = MovieSerializer(
                movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            movie_id = kwargs.get('id')
            serializer = MovieSerializer(Movie.objects.get(pk=movie_id))
            return Response(serializer.data, status=status.HTTP_200_OK)



class SearchMovieByTitleView(APIView):
    def get(self, request, **kwargs):
        if kwargs.get('title'):
            title = kwargs.get('title')
            movies = Movie.objects.filter(title__icontains=title).order_by('-popularity')
            serializer = MovieSerializer(movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

class SearchMovieByGenreView(APIView):
    def get(self, request, **kwargs):
        if kwargs.get('genre'):
            genre = kwargs.get('genre')
            movies = Genre.objects.get(name=genre).genre_movies.all().order_by('-popularity')
            serializer = MovieSerializer(movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

class SearchMovieByKeywordView(APIView):
    def get(self, request, **kwargs):
        if kwargs.get('keyword'):
            keyword = kwargs.get('keyword')
            movies = Movie.objects.filter(keyword__icontains=keyword).order_by('-popularity')
            serializer = MovieSerializer(movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

class SearchActorView(APIView):
    def get(self, request, **kwargs):
        if kwargs.get('actor'):
            actor = kwargs.get('actor')
            actors = Actor.objects.filter(ko_name__icontains=actor)
            serializer = ActorSearchSerializer(actors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

class SearchActorDetailView(APIView):
    def get(self, request, **kwargs):
        if kwargs.get('actor'):
            actor = kwargs.get('actor')
            actor = Actor.objects.filter(id=actor)
            serializer = ActorSerializer(actor, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

class SearchDirectorDetailView(APIView):
    def get(self, request, **kwargs):
        if kwargs.get('director'):
            director = kwargs.get('director')
            director = Director.objects.filter(id=director)
            serializer = DirectorSerializer(director, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

class SearchDirectorView(APIView):
    def get(self, request, **kwargs):
        if kwargs.get('director'):
            director = kwargs.get('director')
            director = Director.objects.filter(ko_name__icontains=director)
            serializer = DirectorSearchSerializer(director, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


class AddMovieScore(APIView):
    def post(self, request):
        movie = request.data
        serializer = MovieScoreSerializer(data=movie)
        if serializer.is_valid():
            serializer.save() #UserSerializer의 유효성 검사를 한 뒤 DB에 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED) #client에게 JSON response 전달
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TrainMovieData(APIView):
    def get(self, request):
        movie_score = MovieScore.objects.all().values()
        movie_score_df = pd.DataFrame(movie_score)
        movie = Movie.objects.all().values()
        movie_df = pd.DataFrame(movie)
        movie_df['id'] = movie_df['id'].astype('int')
        reader = Reader()
        data = Dataset.load_from_df(movie_score_df[['user', 'movie', 'rating']], reader)
        svd = SVD()
        cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
        joblib.dump(svd, './svd1.pkl')
        return Response([{"성공" : "모델링 끝"}], status=status.HTTP_201_CREATED)


def new_title(title):
    special_word = ["\"", "@", ":", "!", "\'", "?", "|"]
    for s_word in special_word:
        title.replace(s_word, "")
    return [title]


def make_date(time):
    time = time.split("-")
    time = int(''.join(time))
    return time

def genre_all(user_search, user):
    weight = {"keyword": 1, "director": 1, "genre": 1, "actor": 1, "movie": 1}
    search_report = []
    user_id = user
    movie_score = MovieScore.objects.all().values()
    movie_score_df = pd.DataFrame(movie_score)
    movie = Movie.objects.all().values()
    movie_df = pd.DataFrame(movie)
    movie_df['id'] = movie_df['id'].astype('int')

    if user_search.exists():
        for search in user_search:
            weight[search.keyword] += 1
            search_report.append(search.word)
            if len(search_report) == 5:
                break

    svd = joblib.load('svd1.pkl')

    movies_in_score = movie_score_df[movie_score_df['movie'].notnull()]['movie'].astype('int')
    movie_df = movie_df[movie_df['id'].isin(movies_in_score)]

    movies_movie = movie_df[movie_df['id'].notnull()]['id'].astype('int')
    movie_score_df = movie_score_df[movie_score_df['movie'].isin(movies_movie)]
    movie_df = movie_df.reset_index()

    movie_df['actor_string'] = movie_df['actor_string'].str.split("|")
    movie_df['keyword'] = movie_df['keyword'].str.split("|")
    movie_df['keyword'] = movie_df['keyword'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])
    movie_df["genre_string"] = movie_df["genre_string"].str.split(" ")
    movie_df["director_string"] = movie_df["director_string"].apply(lambda x: [x])
    movie_df['search_important'] =  movie_df['keyword'] * weight["keyword"] + \
                                    movie_df['genre_string'] * weight["genre"] + \
                                    movie_df["actor_string"] * weight["actor"] + \
                                    movie_df["director_string"] * weight["director"]
    movie_df['important'] = movie_df['keyword'] + movie_df['genre_string'] + \
                            movie_df["actor_string"] + movie_df["director_string"]
    movie_df['search_important'] = movie_df['search_important'].apply(lambda x: ' '.join(x))
    movie_df['important'] = movie_df['important'].apply(lambda x: ' '.join(x))
    count = CountVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
    count_matrix = count.fit_transform(movie_df['important'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    indices = pd.Series(movie_df.index, index=movie_df['id'])

    

    def hybrid(user_id, movie_id):
        idx = indices[movie_id]
        sim_scores = list(enumerate(cosine_sim[int(idx)]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:26]
        movie_indices = [i[0] for i in sim_scores]

        movies = movie_df.iloc[movie_indices][['title', 'id']]
        movies['est'] = movies['id'].apply(lambda x: svd.predict(user_id, x).est)
        movies = movies.sort_values('est', ascending=False)
        return movies.head(10)

    def m_recommend(user_id):
        movies = pd.DataFrame()
        if search_report:
            user_df = pd.DataFrame([" ".join(search_report)], columns=["search_important"])
            important_df = pd.DataFrame(movie_df['search_important'], columns=["search_important"])
            new_movie_df = pd.DataFrame()
            new_movie_df = pd.concat([new_movie_df, user_df])
            new_movie_df = pd.concat([new_movie_df, important_df])
            search_matrix = count.fit_transform(new_movie_df['search_important'])
            search_cosine_sim = cosine_similarity(search_matrix, search_matrix)
            idx = 0
            search_sim_scores = list(enumerate(search_cosine_sim[int(idx)]))
            search_sim_scores = sorted(search_sim_scores, key=lambda x: x[1], reverse=True)
            search_sim_scores = search_sim_scores[1:4]
            search_movie_indices = [i[0] - 1 for i in search_sim_scores]
            search_movies = movie_df.iloc[search_movie_indices][['title', 'id']]
            movies = pd.concat([movies, search_movies])

            search_est_movies = pd.DataFrame()
            for i, row in search_movies.iterrows():
                search_est_movies = pd.concat([search_est_movies, hybrid(user_id, row['id'])])

            search_est_movies = search_est_movies.sort_values("est", ascending=False)
            movie_title = search_est_movies[['title', 'id']]
            movies = pd.concat([movies, movie_title])
            movies = movies['title']
            movies = movies.astype(str).drop_duplicates().head(6)

        user_movies = pd.DataFrame()
        user_movie = movie_score_df[movie_score_df["user"] == user_id].sort_values("rating", ascending=False).head(
            10)
        if not user_movie.empty:
            for i, row in user_movie.iterrows():
                user_movies = pd.concat([user_movies, hybrid(user_id, row["movie"])])
            user_movies = user_movies.sort_values("est", ascending=False)
            user_movies_title = user_movies["title"]
            movies = pd.concat([movies, user_movies_title])
        else:
            all_movie = Movie.objects.all().values()
            all_movie = pd.DataFrame(all_movie)
            all_movie = all_movie.sort_values('vote_count', ascending=False).head(10)
            all_movie_title = all_movie["title"]
            movies = pd.concat([movies, all_movie_title])

        result = movie_df.loc[movies.astype(str).drop_duplicates().index].head(10)

        return result.to_json(orient='records')

    df_json = m_recommend(user_id)
    return Response(json.loads(df_json), status=status.HTTP_201_CREATED)

class RecommendMovie(APIView):
    def get(self, request, **kwargs):
        genre = kwargs.get('genre')
        user = request.user.id
        user_search = Search.objects.filter(user_id = user).order_by('-id')

        if genre == "all":
            return genre_all(user_search, user)
        else:
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d")
            genre_movies = pd.DataFrame()
            movie_score = MovieScore.objects.all().values()
            movie_score_df = pd.DataFrame(movie_score)

            movie = Movie.objects.filter(genre_string__icontains=genre).values()
            movie_df = pd.DataFrame(movie)
            if movie_df.empty:
                return Response([{"실패" : "장르 잘못 입력됨"}], status=status.HTTP_201_CREATED)
            movie_df['id'] = movie_df['id'].astype('int')

            movie_df = movie_df[movie_df['release_date'] != '']
            movie_df['new_time'] = movie_df['release_date'].apply(make_date)
            movie_df = movie_df[movie_df['new_time'] < make_date(dt_string)]
            movie_df = movie_df[movie_df['vote_count'] > 10]

            movie_by_score = movie_df.sort_values('new_time', ascending=False).head(3)

            genre_movies = pd.concat([genre_movies, movie_by_score["title"]])

            pop_movie = movie_df.sort_values('vote_count', ascending=False).head(3)
            genre_movies = pd.concat([genre_movies, pop_movie["title"]])

            all_mean = movie_score_df["rating"].mean()

            count_90 = movie_score_df.groupby("movie")["user"].count().quantile(.9)

            def w_rating(df):
                return (df.mean() * df.count() + all_mean  * count_90) / (df.count() + count_90)

            movies_movie = movie_df[movie_df['id'].notnull()]['id'].astype('int')
            movie_score = movie_score_df.groupby("movie")["rating"].agg(w_rating)
            movie_score = pd.DataFrame(movie_score)
            movie_score = movie_score[movie_score.index.isin(movies_movie)].sort_values("rating", ascending=False).head(10)

            movie_score_title = movie_df[movie_df["id"].isin(movie_score.index)]["title"]
            genre_movies = pd.concat([genre_movies, movie_score_title])

            result = movie_df.loc[genre_movies.drop_duplicates().index].head(10)

            df_json = result.to_json(orient='records')
            return Response(json.loads(df_json), status=status.HTTP_201_CREATED)


