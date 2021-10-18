"""django_practice_new URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views

app_name = 'board'

urlpatterns = [
    # User에 관한 API를 처리하는 view로 Request를 넘김
    # path('get', views.BoardView.get, name='get'),
    # path('post', views.BoardView.post, name='post'),
    # path('put', views.BoardView.put, name='put'),
    # path('delete', views.BoardView.delete, name='delete'),
    path('', views.BoardView.as_view()),
    path('<int:id>', views.BoardView.as_view()),
]
