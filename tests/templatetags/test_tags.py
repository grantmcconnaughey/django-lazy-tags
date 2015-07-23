from django import template


register = template.Library()


@register.simple_tag
def test():
    return '<p>hello world</p>'


@register.simple_tag
def test_with_sleep():
    import time
    time.sleep(3)
    return '<p>done sleeping</p>'


@register.inclusion_tag('tests/inclusion_tag_with_args.html')
def test_with_args(arg, kwarg=None):
    return {
        'arg': arg,
        'kwarg': kwarg
    }


@register.inclusion_tag('tests/inclusion_tag.html')
def inclusion():
    return {'test': 'hello world'}
