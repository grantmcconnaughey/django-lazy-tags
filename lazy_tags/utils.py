import json


def get_tag_html(tag, args=None, kwargs=None):
    lib, tag_name = tag.split('.')

    args_str = ''
    if args:
        args = json.loads(args)
        for arg in args:
            args_str += "'{0}'".format(arg)

    kwargs_str = ''
    if kwargs:
        kwargs = json.loads(kwargs)
        for name, value in kwargs.items():
            kwargs_str += "{0}='{1}' ".format(name, value)

    html = '{{% load {lib} %}}{{% {tag_name} {args} {kwargs} %}}'.format(
        lib=lib, tag_name=tag_name, args=args_str, kwargs=kwargs_str)

    return html
