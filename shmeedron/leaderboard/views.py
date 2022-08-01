from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


from leaderboard.models import Game, Category, Player
from leaderboard.forms import GameSubmitionForm

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

@login_required
def submit_game(request):

    if request.method == 'POST':
        
        form = GameSubmitionForm(request.POST)

        if form.is_valid(): # This should be true since there are no validation steps
            requester_player = request.user.player # the requester is automatically a moderator

            new_game = Game()

            new_game.name = form.cleaned_data['game_name']
            new_game.thumbnail_url = form.cleaned_data['thumbnail_url']

            new_game.save() # have to save to give id

            new_game.moderators.set([requester_player])

            new_game.save()


            return HttpResponseRedirect(reverse('games'))
        
        return HttpResponse(status=500) # If something went wrong


    else:
        form = GameSubmitionForm()

    context = {
        "form":form,
    }

    return render(request, 'game_submition.html', context=context)