from django import template
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden

from .utils import get_tag_html


def tag(request, tag_id):
    html = get_tag_html(tag_id)
    t = template.Template(html)
    c = template.RequestContext(request)

    return HttpResponse(t.render(c))
