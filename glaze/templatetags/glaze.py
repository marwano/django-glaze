
from copy import copy
from django.template import Library
from django.template.loader import render_to_string
from django.core import urlresolvers
from django.conf import settings
from django.utils.safestring import mark_safe
from utile import resolve

register = Library()


@register.filter()
def glaze_site_lookup(path, name):
    try:
        namespace = urlresolvers.resolve(path).namespace
        site = resolve(settings.GLAZE_SITE_LOOKUP[namespace])
        return getattr(site, name)
    except:
        return ''


@register.inclusion_tag('glaze/buttons/submit_row.html', takes_context=True)
def glaze_submit_row(context):
    # Leave the original context unmodified by copying it and calling push.
    ctx = copy(context)
    ctx.push()

    html = render_to_string('glaze/buttons/raw_submit_row.html', None, ctx)
    patterns = dict(
        show_save='name="_save"',
        show_delete_link='class="deletelink"',
        show_save_as_new='name="_saveasnew"',
        show_save_and_add_another='name="_addanother"',
        show_save_and_continue='name="_continue"',
    )
    for key, pattern in patterns.items():
        ctx[key] = pattern in html

    ctx['rendered_buttons'] = [i.render(ctx) for i in ctx['glaze_buttons']]
    return ctx
