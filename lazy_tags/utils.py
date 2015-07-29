import json
from collections import OrderedDict

from django.utils import six


def get_tag_html(tag, args=None, kwargs=None):
    """
    Returns the Django HTML to load the tag library and render the tag.

    Args:
        tag (str): The name of the tag following the 'tag_library.tag_name'
            format.
        args (str): The JSON encoded string representing the args that should
            be passed to the template tag.
        kwargs (str): The JSON encoded string representing the kwargs that
            should be passed to the template tag.
    """
    lib, tag_name = tag.split('.')

    args_str = ''
    if args:
        args = json.loads(args)
        for arg in args:
            if isinstance(arg, six.string_types):
                args_str += "'{0}' ".format(arg)
            else:
                args_str += "{0} ".format(arg)

    kwargs_str = ''
    if kwargs:
        kwargs = OrderedDict(json.loads(kwargs))
        for name, value in kwargs.items():
            if isinstance(value, six.string_types):
                kwargs_str += "{0}='{1}' ".format(name, value)
            else:
                kwargs_str += "{0}={1} ".format(name, value)

    html = '{{% load {lib} %}}{{% {tag_name} {args}{kwargs}%}}'.format(
        lib=lib, tag_name=tag_name, args=args_str, kwargs=kwargs_str)

    return html
