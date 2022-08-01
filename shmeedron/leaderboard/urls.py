from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('games/', views.games, name='games'),
    path('<slug:game_slug>-<int:pk>', views.game, name='game-page'),
    path('<slug:game_slug>-<int:game_pk>/<slug:cat_slug>-<int:cat_pk>', views.category, name='category-page'),
]