import json

from django import template
from django.template.loader import render_to_string
from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse

from ..utils import get_tag_id, set_lazy_tag_data


register = template.Library()


@register.simple_tag
def lazy_tag(tag, *args, **kwargs):
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
    tag_id = get_tag_id()
    set_lazy_tag_data(tag_id, tag, args, kwargs)

    return render_to_string('lazy_tags/lazy_tag.html', {
        'tag_id': tag_id,
        'STATIC_URL': settings.STATIC_URL,
    })


def _render_js(library):
    error_message = getattr(settings, 'LAZY_TAGS_ERROR_MESSAGE', 'An error occurred.')
    template = 'lazy_tags/lazy_tags_{0}.html'.format(library)

    return render_to_string(template, {
        'error_message': error_message,
    })


@register.simple_tag
def lazy_tags_javascript():
    """Outputs the necessary JavaScript to load tags over AJAX."""
    return _render_js('javascript')


@register.simple_tag
def lazy_tags_jquery():
    """Outputs the necessary jQuery to load tags over AJAX."""
    return _render_js('jquery')


@register.simple_tag
def lazy_tags_prototype():
    """Outputs the necessary Prototype to load tags over AJAX."""
    return _render_js('prototype')


@register.simple_tag
def lazy_tags_js():
    """An alias to the JavaScript library specified in settings."""
    library = getattr(settings, 'LAZY_TAGS_AJAX_JS', 'jquery')
    return _render_js(library.lower())
