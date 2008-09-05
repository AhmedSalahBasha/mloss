from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import admin
from django.views.generic.list_detail import object_list

admin.autodiscover()

urlpatterns = patterns('',
    # administration
    (r'^admin/(.*)', admin.site.root),

    # Using cab to browse software
    (r'^software/', include('software.urls')),

    # Using registration
    (r'^accounts/', include('registration.urls')),
    (r'^community/', include('community.urls')),
    (r'^user/', include('user.urls')),

    # Display News and FAQ- simplest possible dynamic page
    (r'^news/', 'forshow.views.newsindex'),
    (r'^faq/', 'forshow.views.faqindex'),

    # redirect the root to news
    #('^$', 'forshow.views.newsindex'),
    ('^$', 'django.views.generic.simple.redirect_to', {'url':'/software/'}),

    # Enable comments
    (r'^comments/', include('django.contrib.comments.urls')),
)

if settings.DEBUG and not settings.PRODUCTION:
	urlpatterns += patterns('',(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),)
