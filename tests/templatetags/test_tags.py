from django import template


register = template.Library()


@register.simple_tag
def test():
    return 'hello world'


@register.inclusion_tag('tests/inclusion_tag_with_args.html')
def test_with_args(arg, kwarg=None):
    return {
        'arg': arg,
        'kwarg': kwarg
    }


@register.inclusion_tag('tests/inclusion_tag.html')
def inclusion():
    return {'test': 'hello world'}
