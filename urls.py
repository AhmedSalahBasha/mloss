from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import admin
from django.views.generic.list_detail import object_list

admin.autodiscover()

urlpatterns = patterns('',
    # administration
    #(r'^admin/(.*)', admin.site.root),
    #(r'^admin/', include(admin.site.urls)),
	
    url(r'^admin/', include(admin.site.urls)),

    # software and revision
    #(r'^software/', include('software.urls')),
    #(r'^revision/', include('revision.urls')),
    (r'^software/', include('software.urls')),
    (r'^revision/', include('revision.urls')),
   

    # Using registration
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^community/', include('community.urls')),
    (r'^user/', include('user.urls')),
    #(r'^accounts/', include('registration.backends.default.urls')),
    #(r'^community/', include('community.urls')),
    #(r'^user/', include('user.urls')),


    # Display News and FAQ- simplest possible dynamic page
    #(r'^news/', 'forshow.views.newsindex'),
    #(r'^faq/', 'forshow.views.faqindex'),
    (r'^news/', 'forshow.views.newsindex'),
    (r'^faq/', 'forshow.views.faqindex'),

    # redirect the root to news
    #('^$', 'forshow.views.newsindex'),
    #('^$', 'django.views.generic.simple.redirect_to', {'url':'/software/'}),
    ('^$', 'django.views.generic.simple.redirect_to', {'url':'/software/'}),

    # Enable comments
    #(r'^comments/', include('django.contrib.comments.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
)

if settings.DEBUG and not settings.PRODUCTION:
    urlpatterns += patterns('',(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),)
