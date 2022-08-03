from django import forms

class GameSubmitionForm(forms.Form):
    game_name = forms.CharField(help_text="Enter the name of the game")
    thumbnail_url = forms.URLField(help_text="Enter a thumbnail for the game, ex: <a href='https://www.igdb.com/games/celeste'>Celeste's<a/> picutre is https://images.igdb.com/igdb/image/upload/t_cover_big/co3byy.png (right click on the thumbnail image)",
        required=False,    
    )

class RunSubmitionForm(forms.Form):
    run_hours = forms.IntegerField(help_text="Hours portion of the run duration")
    run_minutes = forms.IntegerField(help_text="Hours portion of the run duration")
    run_seconds = forms.IntegerField(help_text="Hours portion of the run duration")
    run_miliseconds = forms.IntegerField(help_text="Hours portion of the run duration")

    video_url = forms.URLField(help_text="Link to the video. Currently supported: youtube.com, youtu.be, twitch.tv")
    description = forms.CharField(max_length=1000)
    run_date = forms.DateField()

class VerificationDecisionForm(forms.Form):
    run_id = forms.IntegerField()
    decision = forms.CharField(max_length=1)