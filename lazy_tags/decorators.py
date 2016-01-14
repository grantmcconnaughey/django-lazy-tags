from functools import wraps

from django.conf import settings
from django.template.loader import render_to_string
from django.utils import six

from .utils import get_tag_id, set_lazy_tag_data


def _get_func_name(func):
    if six.PY2:
        return func.func_name
    else:
        return func.__name__


def lazy_tag(func=None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        render_tag = kwargs.pop('render_tag', False)

        if render_tag:
            return func(*args, **kwargs)
        else:
            # Set render_tag in the kwargs so the tag will be rendered next
            # time this is called
            tag_lib = func.__module__.partition('templatetags.')[-1]
            tag_name = _get_func_name(func)
            tag = tag_lib + '.' + tag_name
            kwargs['render_tag'] = True
            tag_id = get_tag_id()
            set_lazy_tag_data(tag_id, tag, args, kwargs)

            return render_to_string('lazy_tags/lazy_tag.html', {
                'tag_id': tag_id,
                'STATIC_URL': settings.STATIC_URL,
            })
    return wrapper
