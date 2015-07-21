import json

from django import template
from django.http import HttpResponse


def tag(request):
    lib, tag_name = request.GET['tag'].split('.')

    args_str = ''
    args = request.GET.get('args', [])
    if args:
        args = json.loads(args)
        for arg in args:
            args_str += (" '" + arg + "' ")

    kwargs_str = ''
    kwargs = request.GET.get('kwargs')
    if kwargs:
        kwargs = json.loads(kwargs)
        for name, value in kwargs.iteritems():
            kwargs_str += " {}='{}' ".format(name, value)

    html = '{{% load {lib} %}}{{% {tag_name}{args}{kwargs} %}}'.format(
        lib=lib, tag_name=tag_name, args=args_str, kwargs=kwargs_str)
    t = template.Template(html)
    c = template.Context()

    return HttpResponse(t.render(c))
