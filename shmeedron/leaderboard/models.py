from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100)

class Game(models.Model):
    """Model representing a game (single entry)."""
    name = models.CharField(max_length=100)
    moderators = models.ManyToManyField(Player)

class Submition(models.Model):
    """Model representing a speedrun submition."""
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    time = models.DurationField()

    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True)
    play_date = models.DateField(null=True, blank=True)

    verifier = models.ForeignKey(Player, related_name="verifyer", on_delete=models.SET_NULL, null=True, blank=True)
    verification_date = models.DateField(null=True, blank=True)

    description = models.TextField(max_length=1000)
    video_link = models.URLField(max_length=400)

    SUBMITION_STATUS = (
        ('p', 'Pending'),
        ('v', 'Verified'),
        ('d', 'denied'),
    )

    status = models.CharField(max_length=1, choices=SUBMITION_STATUS, blank=True, default='p', help_text='Submition Status')

    def __str__(self):
        return (self.game.name + " in " + str(self.time) + " by " + self.player.username)

class Category(models.Model):
    """Model representing a category of a game (Any% vs 100%)."""
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=10000)
    rules = models.TextField(max_length=10000)