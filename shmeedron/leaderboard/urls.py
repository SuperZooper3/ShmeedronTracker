from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/games', views.index, name='games'),
]