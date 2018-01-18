try:
    # Removed in Django 1.6
    from django.conf.urls.defaults import url, include
except ImportError:
    from django.conf.urls import url, include

try:
    # Relocated in Django 1.6
    from django.conf.urls.defaults import patterns
except ImportError:
    # Completely removed in Django 1.10
    try:
        from django.conf.urls import patterns
    except ImportError:
        patterns = None

from . import views

_patterns = [
    url(r'^$', views.test_jquery, name='lazy_tags_jquery'),
    url(r'^js/$', views.test_javascript, name='lazy_tags_javascript'),
    url(r'^prototype/$', views.test_prototype, name='lazy_tags_prototype'),
    url(r'^lazy_tags/', include('lazy_tags.urls')),
]

if patterns is None:
    urlpatterns = _patterns
else:
    urlpatterns = patterns('', *_patterns)
