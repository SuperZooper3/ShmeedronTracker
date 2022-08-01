from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from leaderboard.models import Game, Category

# Create your views here.
def index(request):
    
    context = {}
    
    return render(request, 'index.html', context=context)

def games(request):

    context = {
        "games":Game.objects.order_by('name'),
        "row_number":4, # The number of games per row
    }

    return render(request, 'games.html', context=context)

def game(request, game_slug, pk):
    game = get_object_or_404(Game, pk=pk)

    context = {
        "game":game,
        "categories":game.category_set.all,
    }

    return render(request, 'game_page.html', context=context)

def category(request, game_slug, game_pk, cat_slug, cat_pk):
    game = get_object_or_404(Game, pk=game_pk)
    category = get_object_or_404(Category, pk=cat_pk)

    context = {
        "game":game,
        "category":category,
    }

    return render(request, 'cat_page.html', context=context)