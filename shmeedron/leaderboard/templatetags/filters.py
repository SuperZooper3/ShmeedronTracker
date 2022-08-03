from django import template
import datetime

register = template.Library()

def timeclean(value):
    """Strips the leading and trailing 0s from a time object and returns it's string. Arg is irrelevant"""
    assert(type(value)) == datetime.timedelta

    total = value.total_seconds()
    hours = int(total // 3600)
    minutes = int((total % 3600) // 60)
    seconds = int(total % 60)
    miliseconds = int((total % 1) * 1000)

    if hours == 0:
        return '{:02}:{:02}.{:03}'.format(minutes, seconds, miliseconds)
    else:
        return '{}:{:02}:{:02}.{:03}'.format(hours, minutes, seconds, miliseconds).lstrip("0:")

def index(indexable, i):
    return indexable[i]

register.filter("timeclean",timeclean)
register.filter("index",index)