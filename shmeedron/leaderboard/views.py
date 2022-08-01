from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from leaderboard.models import Game

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

def game(request, pk):
    
    context = {
        "game":get_object_or_404(Game, pk=pk)
    }

    return render(request, 'game_page.html', context=context)
