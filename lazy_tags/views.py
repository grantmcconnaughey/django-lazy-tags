import json

from django import template
from django.http import HttpResponse

from .utils import get_tag_html


def tag(request):
    html = get_tag_html(request.GET['tag'],
                        request.GET.get('args'),
                        request.GET.get('kwargs'))
    t = template.Template(html)
    c = template.Context()

    return HttpResponse(t.render(c))
