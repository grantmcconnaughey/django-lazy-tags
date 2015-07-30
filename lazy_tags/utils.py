from django.conf import settings
from django.core.cache import cache
from django.utils import six


def get_cache_key(tag_id):
    """Returns a cache key based on a tag id"""
    return 'lazy_tags_{0}'.format(tag_id)


def set_lazy_tags_cache(tag_id, tag, args=None, kwargs=None):
    """Sets the lazy tags cache for an instance of a lazy tag."""
    tag_context = {
        'tag': tag,
        'args': args,
        'kwargs': kwargs,
    }

    key = get_cache_key(tag_id)
    cache_timeout = getattr(settings, 'LAZY_TAGS_CACHE_TIMEOUT', 3600)
    cache.set(key, tag_context, cache_timeout)


def get_tag_html(tag_id):
    """
    Returns the Django HTML to load the tag library and render the tag.

    Args:
        tag_id (str): The tag id for the to return the HTML for.
    """
    key = get_cache_key(tag_id)
    tag_data = cache.get(key)
    cache.delete(key)
    tag = tag_data['tag']
    args = tag_data['args']
    kwargs = tag_data['kwargs']

    lib, tag_name = tag.split('.')

    args_str = ''
    if args:
        for arg in args:
            if isinstance(arg, six.string_types):
                args_str += "'{0}' ".format(arg)
            else:
                args_str += "{0} ".format(arg)

    kwargs_str = ''
    if kwargs:
        for name, value in kwargs.items():
            if isinstance(value, six.string_types):
                kwargs_str += "{0}='{1}' ".format(name, value)
            else:
                kwargs_str += "{0}={1} ".format(name, value)

    html = '{{% load {lib} %}}{{% {tag_name} {args}{kwargs}%}}'.format(
        lib=lib, tag_name=tag_name, args=args_str, kwargs=kwargs_str)

    return html
