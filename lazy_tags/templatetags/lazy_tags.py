import json
import uuid
from django import template
from django.core.urlresolvers import reverse


register = template.Library()


@register.simple_tag
def lazy_tag(tag, *args, **kwargs):
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
    args_str = json.dumps(args or [])
    kwargs_str = json.dumps(kwargs or {})
    tag_url = reverse("lazy_tag")
    id = str(uuid.uuid4())

    html = """
        <div id="{id}"></div>
        <script type="text/javascript">
            $(function() {{
                $.ajax({{
                    type: "GET",
                    url: "{url}",
                    data: {{
                        tag: "{tag}",
                        args: {args},
                        kwargs: {kwargs},
                    }},
                    success: function(data) {{
                        $('#{id}').html(data);
                    }}
                }});
            }});
        </script>
    """
    html = html.format(id=id, url=tag_url, tag=tag, args=args_str,
        kwargs=kwargs_str)

    return html
