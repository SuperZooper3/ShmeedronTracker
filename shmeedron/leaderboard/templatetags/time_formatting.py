from django import template
import datetime

register = template.Library()

def timeclean(value):
    """Strips the leading and trailing 0s from a time object and returns it's string. Arg is irrelevant"""
    assert(type(value)) == datetime.timedelta
    time_string = str(value)
    out_string = ""
    write_buffer = ""
    non_values = ["0",":"]
    milisecond_flag = "."
    writing = False
    miliseconds = False

    for v in time_string:
        if v not in non_values:
            writing = True
        
        if writing:
            write_buffer += v
            if v == milisecond_flag:
                miliseconds = True

            if v not in non_values or not miliseconds:
                out_string += write_buffer
                write_buffer = ""

    return out_string

# print(clean_time(datetime.timedelta(minutes=10, hours=0, seconds=0, milliseconds=15)))
register.filter("timeclean",timeclean)