# This file was taken from the following tutorial:
# https://learndjango.com/tutorials/django-markdown-tutorial
# Accessed 26/08/2020

from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])