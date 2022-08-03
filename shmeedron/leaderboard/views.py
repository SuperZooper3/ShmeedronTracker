from copy import deepcopy
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

from leaderboard.models import Game, Category, Player, Submition
from leaderboard.forms import GameSubmitionForm, RunSubmitionForm, VerificationDecisionForm

from .utils import video_url_parse, get_player, reverse_querystring
import datetime

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
    runs = list(category.submition_set.all().filter(status__exact = "v").order_by("time"))

    # Process the runs to only include a player's best time, unless the obsolete tag is true
    obsolete = (request.GET.get('obsolete', '').lower() == 'true')
    if not obsolete:
        temp = deepcopy(runs)
        runs = []
        players = []

        for run in temp:
            if run.player.id not in players:
                runs.append(run)
                players.append(run.player.id)
    
        obsolete_link = reverse_querystring('category-page',
            args=(slugify(category.game.name),str(category.game.id),slugify(category.name),str(category.id)),
            query_kwargs={'obsolete': 'true'},
            )
    else:
        obsolete_link = reverse_querystring('category-page',
            args=(slugify(category.game.name),str(category.game.id),slugify(category.name),str(category.id)),
            query_kwargs={'obsolete': 'false'},
            )

    context = {
        "game":game,
        "category":category,
        "runs":runs,
        "obsolete":obsolete,
        "obsolete_link":obsolete_link,

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

def player(request, username_slug, pk): # The pk is a User pk, not a player PK
    # If a player for the user requested dosen't exist, make it with their username as the display name
    player = get_player(get_object_or_404(User,pk=pk))

    runs = player.submition_set.all()
    print(runs)
    
    context = {
        "player":player,
    }

    return render(request, 'player.html', context=context)

def run(request, pk):
    run_object = get_object_or_404(Submition, pk=pk)
    embed_src = video_url_parse(run_object.video_link)
    
    context = {
        "run":run_object,
        "embed_src":embed_src,
    }

    return render(request, 'run_page.html', context=context)

@login_required
def submit_run(request, cat_pk):
    category_object = get_object_or_404(Category, pk=cat_pk)
    
    if request.method == 'POST':
        
        form = RunSubmitionForm(request.POST)

        if form.is_valid(): 
            new_submition = Submition()

            run_time = datetime.timedelta(
                hours=form.cleaned_data["run_hours"],
                minutes=form.cleaned_data["run_minutes"],
                seconds=form.cleaned_data["run_seconds"],
                milliseconds=form.cleaned_data["run_miliseconds"],
            )

            new_submition.time = run_time
            new_submition.description = form.cleaned_data["description"]
            new_submition.play_date = form.cleaned_data["run_date"]
            new_submition.video_link = form.cleaned_data["video_url"]
            new_submition.player =  get_player(request.user)
            new_submition.category = category_object

            new_submition.save()

            return HttpResponseRedirect(reverse('category-page',args=(
            slugify(category_object.game.name),str(category_object.game.id),slugify(category_object.name),str(category_object.id)
            )))

    else:
        proposed_date = datetime.date.today()
        form = RunSubmitionForm(initial={'run_date':proposed_date})

    context = {
        "form":form,
        "category":category_object,
    }

    return render(request, 'run_submition.html', context=context)

@login_required
def verify_main(request):
    player = get_player(request.user)

    games = list(player.game_set.all().order_by("name"))

    context = {
        "games":games,
    }

    return render(request, 'verify_main.html', context=context)

@login_required
def verify_game(request, game_slug, game_pk):
    
    player = get_player(request.user)
    game = get_object_or_404(Game, pk=game_pk)

    if player not in game.moderators.all():
        return HttpResponse('Unauthorized', status=401)

    categorys = game.category_set.all()
    
    queue = []

    for cat in categorys:
        queue.extend(
            list(
               cat.submition_set.all().filter(status__exact = "p").order_by("play_date")
            )
        )

    embed_src = []

    for run in queue:
        embed_src.append(
            video_url_parse(run.video_link)
        )

    print(queue,embed_src)

    context = {
        "game":game,
        "queue":queue,
        "embed_src":embed_src,
    }

    return render(request, 'verify_game.html', context=context)

@login_required
def verify_run(request, run_pk):
    
    player = get_player(request.user)
    run = get_object_or_404(Submition, pk=run_pk)

    if player not in run.category.game.moderators.all():
        return HttpResponse('Unauthorized', status=401)

    if request.method == 'POST':
        
        form = VerificationDecisionForm(request.POST)

        if form.is_valid(): 
            run.status = "v"
            run.verifier = player
            run.verification_date = datetime.datetime.today()

            run.save()

            return HttpResponseRedirect(reverse('verify-main'))
        
        return HttpResponseRedirect(reverse('verify-run', run_pk))

    else:
        form = VerificationDecisionForm(initial={'run_id':run_pk,"decision":"v"})

    context = {
        "run":run,
        "form":form,
    }

    return render(request, 'verify_run.html', context=context)

@login_required
def deny_run(request, run_pk):

    player = get_player(request.user)
    run = get_object_or_404(Submition, pk=run_pk)

    if player not in run.category.game.moderators.all():
        return HttpResponse('Unauthorized', status=401)

    if request.method == 'POST':
        
        form = VerificationDecisionForm(request.POST)

        if form.is_valid(): 
            run.status = "d"
            run.verifier = player
            run.verification_date = datetime.datetime.today()

            run.save()

            return HttpResponseRedirect(reverse('verify-main'))
        
        return HttpResponseRedirect(reverse('deny-run', run_pk))

    else:
        form = VerificationDecisionForm(initial={'run_id':run_pk,"decision":"d"})

    context = {
        "run":run,
        "form":form,
    }

    return render(request, 'deny_run.html', context=context)