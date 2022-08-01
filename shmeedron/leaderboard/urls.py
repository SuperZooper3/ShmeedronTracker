from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('games/', views.games, name='games'),
    path('game/<int:pk>', views.game, name='game-page'),
]