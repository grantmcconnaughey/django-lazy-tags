try:
    from django.conf.urls import patterns, include
except ImportError:
    from django.conf.urls.defaults import patterns, include


urlpatterns = patterns(
    '',
    (r'^lazy_tags/', include('lazy_tags.urls')),
)
