from django.urls import path, include
from . import views

app_name = 'movie'

urlpatterns = [
    path('', views.MovieView.as_view()),
    path('<int:id>', views.MovieView.as_view()),
    path('search/title/<str:title>', views.SearchMovieByTitleView.as_view()),
    path('search/genre/<str:genre>', views.SearchMovieByGenreView.as_view()),
    path('search/actor/<str:actor>', views.SearchActorView.as_view()),
    path('search/director/<str:director>', views.SearchDirectorView.as_view()),
    path('search/actor/detail/<int:actor>', views.SearchActorDetailView.as_view()),
    path('search/director/detail/<int:director>', views.SearchDirectorDetailView.as_view()),
    path('search/keword/<str:keyword>', views.SearchMovieByKeywordView.as_view()),
    path('add/',views.AddMovieScore.as_view()),
    path('recommend/<str:genre>', views.RecommendMovie.as_view()),
    path('train/', views.TrainMovieData.as_view()),
]