from django import template
import datetime
import time
register = template.Library()


def print_timestamp(timestamp):
    #     try:
    #         # assume, that timestamp is given in seconds with decimal point
    #         ts = float(timestamp)
    #     except ValueError:
    #         return None
    #     return datetime.datetime.fromtimestamp(ts)
    return time.strftime("%Y-%m-%d", time.gmtime(timestamp))

register.filter(print_timestamp)
