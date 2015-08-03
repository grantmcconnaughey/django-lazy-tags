from functools import wraps

from django.conf import settings
from django.template.loader import render_to_string

from .utils import get_tag_id, set_lazy_tag_data


def lazy_tag(func=None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tag_name = func.func_name
        tag_lib = func.__module__.split('.')[-1]
        tag = tag_lib + '.' + tag_name
        render_tag = kwargs.pop('render_tag', False)
        if render_tag:
            return func(*args, **kwargs)
        else:
            # Set render_tag in the kwargs so the tag will be rendered next
            # time this is called
            kwargs['render_tag'] = True
            tag_id = get_tag_id()
            set_lazy_tag_data(tag_id, tag, args, kwargs)

            return render_to_string('lazy_tags/lazy_tag.html', {
                'tag_id': tag_id,
                'STATIC_URL': settings.STATIC_URL,
            })
    return wrapper
