from django.conf.urls import patterns, include, url
from auth.views import Register, Login, UserInfoHandler, Logout
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from auth.api import MyUserResource
from demo import  settings

admin.autodiscover()

my_user_resource = MyUserResource()

urlpatterns = patterns('',
    url(r'^$', 'auth.views.index', name='index'),
    url(r'^register$', Register(), name='register'),
    url(r'^login$', Login()),
    url(r'^user_info$', UserInfoHandler()),
    url(r'^logout$', Logout()),
    #url(),
    # Examples:
    # url(r'^$', 'demo.views.home', name='home'),
    # url(r'^demo/', include('demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(my_user_resource.urls)),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
    )
print settings.STATIC_ROOT

