from django import template

from lazy_tags.decorators import lazy_tag


register = template.Library()


@register.simple_tag
def test():
    return '<p>hello world</p>'


@register.simple_tag
@lazy_tag
def test_decorator():
    return 'Success!'


@register.simple_tag
@lazy_tag
def test_simple_dec_args(arg, kwarg=None):
    return '{0} {1}'.format(arg, kwarg)


@register.inclusion_tag('tests/decorator_tag_with_args.html')
@lazy_tag
def test_decorator_with_args(arg, kwarg=None):
    return {
        'arg': arg,
        'kwarg': kwarg
    }


@register.simple_tag
def test_with_sleep():
    import time
    time.sleep(2)
    return '<ul style="text-align: left;"><li>Steve Jobs</li><li>Bill Gates</li><li>Elon Musk</li></ul>'


@register.inclusion_tag('tests/inclusion_tag_with_args.html')
def test_with_args(arg, kwarg=None):
    return {
        'arg': arg,
        'kwarg': kwarg
    }


@register.simple_tag
def test_orm(user):
    return '<p>{} | {}</p>'.format(user.username, user.email)


@register.inclusion_tag('tests/inclusion_tag.html')
def inclusion():
    return {'test': 'hello world'}
