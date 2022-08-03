from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('games/', views.games, name='games'),
    path('games/submit', views.submit_game, name='submit-game'),
    path('<slug:game_slug>-<int:pk>', views.game, name='game-page'),
    path('<slug:game_slug>-<int:game_pk>/<slug:cat_slug>-<int:cat_pk>', views.category, name='category-page'),
    path('player/<slug:username_slug>-<int:pk>', views.player, name='player'),
    path('run/<int:pk>', views.run, name='run-page'),
    path('run/submit/<int:cat_pk>', views.submit_run, name='submit-run'),
    path('verify/', views.verify_main, name='verify-main'),
    path('verify/<slug:game_slug>-<int:game_pk>', views.verify_game, name='verify-game'),
    path('verify/<int:run_pk>', views.verify_run, name='verify-run'),
    path('verify/deny/<int:run_pk>', views.deny_run, name='deny-run'),
]