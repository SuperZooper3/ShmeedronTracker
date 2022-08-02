from urllib.parse import urlparse, parse_qsl
from django.core.exceptions import ObjectDoesNotExist 
from django.contrib.auth.models import User
from leaderboard.models import Player
from django.utils.http import urlencode
from django.urls import reverse


def video_url_parse(url):
    """Takes in a video url (youtube, twitch (more could be added later)) and returns an embed iFrame """
    try:
        parsed = urlparse(url)
        
        if "youtube.com" in parsed.netloc and parsed.path == "/watch":
            query_args = dict(parse_qsl(parsed.query))
            video_slug = query_args["v"]
            return f"https://www.youtube.com/embed/{video_slug}"
            

        elif "youtu.be" in parsed.netloc: #Youtube shortened format
            video_slug = parsed.path.replace("/","")
            return f"https://www.youtube.com/embed/{video_slug}"

        elif "twitch.tv" in parsed.netloc and "/videos" in parsed.path:
            video_slug = parsed.path[(parsed.path.index("/videos/") + len("/videos/")):]
            return f"https://player.twitch.tv/?video=v{video_slug}&parent=127.0.0.1" # The parent attribute here needs to have a better way to dynamically choose it

    except:
        return -1

def get_player(user):

    try:
        player = user.player
    
    except (ObjectDoesNotExist):    
        player = Player()
        player.display_name = user.username
        player.user_id = user.id
        player.save()

    return player

# From https://gist.github.com/benbacardi/227f924ec1d9bedd242b
def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
    '''Custom reverse to handle query strings.
    Usage:
        reverse('app.views.my_view', kwargs={'pk': 123}, query_kwargs={'search': 'Bob'})
    '''
    base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url