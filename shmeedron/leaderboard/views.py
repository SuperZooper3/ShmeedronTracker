from django.shortcuts import render

# Create your views here.
def index(request):
    context = {}
    return render(request, 'index.html', context=context)

def games(request):
    context = {}
    return render(request, 'games.html', context=context)
