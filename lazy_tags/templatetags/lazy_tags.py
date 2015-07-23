import json
import uuid
from django import template
from django.template.loader import render_to_string
from django.conf import settings
from django.core.urlresolvers import reverse


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
    # Gross hack to pollute the parent context so lazy_tag_data can be accessed
    # from the lazy_tags_javascript tag
    c = context.dicts[0]
    if not c.get('lazy_tag_data'):
        c['lazy_tag_data'] = {}

    tag_id = str(uuid.uuid4())
    c['lazy_tag_data'][tag_id] = {
        'tag': tag,
        'args': json.dumps(args or []),
        'kwargs': json.dumps(kwargs or {}),
    }

    return render_to_string('lazy_tags/lazy_tag.html', {
        'id': tag_id,
        'STATIC_URL': settings.STATIC_URL,
    })


@register.simple_tag(takes_context=True)
def lazy_tags_js(context):
    """Outputs the necessary JavaScript to load tags over AJAX."""
    tag_url = reverse("lazy_tag")
    lazy_tag_data = context.get('lazy_tag_data')
    error_message = 'An error occurred.'
    if hasattr(settings, 'LAZY_TAGS_ERROR_MESSAGE'):
        error_message = getattr(settings, 'LAZY_TAGS_ERROR_MESSAGE')

    return render_to_string('lazy_tags/lazy_tags_js.html', {
        'lazy_tag_data': lazy_tag_data,
        'tag_url': tag_url,
        'error_message': error_message,
    })
