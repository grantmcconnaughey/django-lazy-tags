from django.conf.urls import patterns, url
from .views import tag

urlpatterns = patterns(
    '',
    url(r'^tag/(?P<tag_id>.+)$', tag, name='lazy_tag')
)
