from django import template
from django.conf import settings
import os

register = template.Library()


@register.simple_tag
def viz(file):
    return os.path.join(settings.VIZ_URL, file)
