try:
    from django.conf.urls import patterns, include, url
except ImportError:
    from django.conf.urls.defaults import patterns, include, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.test, name='lazy_tags_test'),
    url(r'^lazy_tags/', include('lazy_tags.urls')),
)
