from django import template


register = template.Library()


@register.simple_tag
def test_nested():
    return '<p>hello world</p>'
