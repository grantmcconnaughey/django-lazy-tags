from django import template
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden

from .utils import get_tag_html


def tag(request, tag_id):
    force_login = getattr(settings, 'LAZY_TAGS_FORCE_LOGIN', False)
    if force_login:
        if not request.user.is_authenticated():
            return HttpResponseForbidden()

    html = get_tag_html(tag_id)
    t = template.Template(html)
    c = template.RequestContext(request)

    return HttpResponse(t.render(c))
