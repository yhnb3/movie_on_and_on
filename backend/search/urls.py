from django.urls import path, include
from . import views

app_name = 'search'

urlpatterns = [
    path('save/', views.SaveSearchView.as_view(), name="saveSearch")
]
