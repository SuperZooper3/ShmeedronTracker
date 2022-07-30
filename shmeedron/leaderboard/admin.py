from django.contrib import admin

# Register your models here.

from .models import Game, Submition, Player, Category

admin.site.register(Game)
admin.site.register(Category)
admin.site.register(Submition)
admin.site.register(Player)