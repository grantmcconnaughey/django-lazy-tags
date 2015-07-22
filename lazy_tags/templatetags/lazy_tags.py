import json
import uuid
from django import template
from django.core.urlresolvers import reverse


register = template.Library()


@register.simple_tag(takes_context=True)
def lazy_tag(context, tag, *args, **kwargs):
    """
    Lazily loads a template tag after the page has loaded. Requires jQuery
    (for now).

    Usage:
        {% load lazy_tags %}

        {% lazy_tag 'tag_lib.tag_name' arg1 arg2 kw1='test' kw2='hello' %}

    Args:
        tag (str): the tag library and tag name separated by a period. For a
            template tag named `do_thing` in a tag library named `thing_tags`
            the `tag` argument would be `'thing_tags.doc_thing'`.
        *args: arguments to be passed to the template tag.
        **kwargs:  keyword arguments to be passed to the template tag.
    """
    c = context.dicts[0]
    if not c.get('lazy_tag_data'):
        c['lazy_tag_data'] = {}

    id = str(uuid.uuid4())
    c['lazy_tag_data'][id] = {
        'tag': tag,
        'args': args,
        'kwargs': kwargs,
    }

    html = '<div id="{id}"></div>'.format(id=id)

    return html


@register.simple_tag(takes_context=True)
def lazy_tags_javascript(context):
    html = ''
    tag_url = reverse("lazy_tag")

    for tag_id, data in context.get('lazy_tag_data', {}).iteritems():
        tag = data.get('tag')
        args = data.get('args')
        kwargs = data.get('kwargs')
        args_str = json.dumps(args or [])
        kwargs_str = json.dumps(kwargs or {})

        if not html:
            html = """
                <script type="text/javascript">
                    $(function() {
            """

        js = """
            $.ajax({{
                type: "GET",
                url: "{url}",
                data: {{
                    tag: "{tag}",
                    args: JSON.stringify({args}),
                    kwargs: {kwargs},
                }},
                success: function(data) {{
                    $('#{id}').html(data);
                }}
            }});
        """
        js = js.format(
            id=tag_id, url=tag_url, tag=tag, args=args_str, kwargs=kwargs_str)

        html += js

    if html:
        html += '});</script>'

    return html
