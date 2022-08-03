from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.utils.text import slugify
from django.contrib.auth.models import User
from .templatetags.filters import timeclean

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100)

    class Meta:
        ordering = ['display_name']

    def get_absolute_url(self):
        return reverse('player', args=[str(self.display_name),str(self.user.id)])

    def __str__(self):
        return self.display_name

class Game(models.Model):
    """Model representing a game (single entry)."""
    name = models.CharField(max_length=100) 
    moderators = models.ManyToManyField(Player)

    thumbnail_url = models.URLField(max_length=400, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        """Returns the URL to access the game page for a specific game."""
        return reverse('game-page', args=[slugify(str(self.name)), str(self.id)])

    def __str__(self):
        return self.name

class Category(models.Model):
    """Model representing a category of a game (Any% vs 100%)."""
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=10000)
    rules = models.TextField(max_length=10000)

    class Meta:
        ordering = ['game','name']

    def get_absolute_url(self):
        """Returns the URL to access the game page for a specific game."""
        return reverse('category-page', args=[slugify(str(self.game.name)),str(self.game.id),slugify(str(self.name)),str(self.id)])

    def __str__(self):
        return f"{self.name} ({self.game})"

class Submition(models.Model):
    """Model representing a speedrun submition."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    time = models.DurationField()

    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True)
    play_date = models.DateField(null=True, blank=True)

    verifier = models.ForeignKey(Player, related_name="verifier", on_delete=models.SET_NULL, null=True, blank=True)
    verification_date = models.DateField(null=True, blank=True)

    description = models.TextField(max_length=1000, null=True, blank=True)
    video_link = models.URLField(max_length=500)

    SUBMITION_STATUS = (
        ('p', 'Pending'),
        ('v', 'Verified'),
        ('d', 'Denied'),
    )

    status = models.CharField(max_length=1, choices=SUBMITION_STATUS, blank=True, default='p', help_text='Submition Status')

    class Meta:
        ordering = ['time']

    def get_absolute_url(self):
        return reverse('run-page', args=[str(self.id)])

    def __str__(self):
        return (str(self.category) + " in " + timeclean(self.time) + " by " + str(self.player.display_name))