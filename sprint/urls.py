from django.conf import settings
from django.conf.urls import patterns, url


urlpatterns = patterns('sprint.views',
    url(r'^$', 'home', name='home'),
    url(r'^contact$', 'contact', name='contact'),
    url(r'^contact/done$', 'contact_done', name='contact_done'),
)

if not settings.DEBUG:
    static_opts = {'document_root': settings.STATIC_ROOT}
    urlpatterns += patterns('django.views.static',
        url(r'^static/(?P<path>.*)$', 'serve', static_opts),
    )
