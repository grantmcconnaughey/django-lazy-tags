from django.conf.urls import url

from .views import tag

urlpatterns = [
    url(r'^tag/(?P<tag_id>.+)?$', tag, name='lazy_tag'),
]
