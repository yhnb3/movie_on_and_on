from django.urls import path, include
from . import views

app_name = 'review'

urlpatterns = [
    path('', views.ReviewView.as_view()),
    # path('create/', views.CreateView.as_view(), name='create'),
    path('<int:id>', views.ReviewView.as_view()),

]
