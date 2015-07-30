import json
import uuid

from django import template
from django.template.loader import render_to_string
from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse

from ..utils import set_lazy_tags_cache


register = template.Library()


@register.simple_tag(takes_context=True)
def lazy_tag(context, tag, *args, **kwargs):
    """
    Lazily loads a template tag after the page has loaded. Requires jQuery
    (for now).

    Usage:
        {% load lazy_tags %}

        {% lazy_tag 'tag_lib.tag_name' arg1 arg2 kw1='test' kw2='hello' %}

    Args:
        tag (str): the tag library and tag name separated by a period. For a
            template tag named `do_thing` in a tag library named `thing_tags`
            the `tag` argument would be `'thing_tags.doc_thing'`.
        *args: arguments to be passed to the template tag.
        **kwargs:  keyword arguments to be passed to the template tag.
    """
    tag_id = str(uuid.uuid4())
    set_lazy_tags_cache(tag_id, tag, args, kwargs)

    # Gross hack to pollute the parent context so lazy_tag_ids can be accessed
    # from the lazy_tags_javascript tag
    c = context.dicts[0]
    if not c.get('lazy_tag_ids'):
        c['lazy_tag_ids'] = []
    c['lazy_tag_ids'].append(tag_id)

    return render_to_string('lazy_tags/lazy_tag.html', {
        'tag_id': tag_id,
        'STATIC_URL': settings.STATIC_URL,
    })


@register.simple_tag(takes_context=True)
def lazy_tags_js(context):
    """Outputs the necessary JavaScript to load tags over AJAX."""
    lazy_tag_ids = context.get('lazy_tag_ids')
    error_message = 'An error occurred.'
    if hasattr(settings, 'LAZY_TAGS_ERROR_MESSAGE'):
        error_message = getattr(settings, 'LAZY_TAGS_ERROR_MESSAGE')

    return render_to_string('lazy_tags/lazy_tags_js.html', {
        'lazy_tag_ids': lazy_tag_ids,
        'error_message': error_message,
    })
