try:
    from django.conf.urls import patterns, include, url
except ImportError:
    from django.conf.urls.defaults import patterns, include, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.test, name='lazy_tags_jquery'),
    url(r'^js/$', views.test_javascript, name='lazy_tags_javascript'),
    url(r'^prototype/$', views.test_prototype, name='lazy_tags_prototype'),
    url(r'^lazy_tags/', include('lazy_tags.urls')),
)
