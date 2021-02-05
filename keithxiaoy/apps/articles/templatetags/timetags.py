from django import template
import datetime
from django.template.defaultfilters import stringfilter
import markdown as md

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


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])


register.filter(markdown)
