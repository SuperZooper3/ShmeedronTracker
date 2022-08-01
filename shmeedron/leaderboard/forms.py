from django import forms

class GameSubmitionForm(forms.Form):
    game_name = forms.CharField(help_text="Enter the name of the game")
    thumbnail_url = forms.URLField(help_text="Enter a thumbnail for the game, ex: <a href='https://www.igdb.com/games/celeste'>Celeste's<a/> picutre is https://images.igdb.com/igdb/image/upload/t_cover_big/co3byy.png (right click on the thumbnail image)",
        required=False,    
    )
