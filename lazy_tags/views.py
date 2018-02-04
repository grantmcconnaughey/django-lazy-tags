from django import template
from django.http import HttpResponse

from .utils import get_tag_html


def tag(request, tag_id=None):
    """
    The view used to render a tag after the page has loaded.
    """
    html = get_tag_html(tag_id)
    t = template.Template(html)
    c = template.RequestContext(request)

    return HttpResponse(t.render(c))
