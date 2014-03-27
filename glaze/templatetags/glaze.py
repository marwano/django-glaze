
from django import template
from django.core import urlresolvers
from django.conf import settings
from utile import resolve

register = template.Library()


@register.filter()
def glaze_site_lookup(path, name):
    try:
        namespace = urlresolvers.resolve(path).namespace
        site = resolve(settings.GLAZE_SITE_LOOKUP[namespace])
        return getattr(site, name)
    except:
        return ''
