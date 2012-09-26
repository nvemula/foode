from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^',include("foode.apps.restaurants.urls")),
             url(r'^(?P<slug>\w+)/$', 'restaurant', name="describe_restaurant"),#restaurant details page
    # Examples:
    # url(r'^$', 'foode.views.home', name='home'),
    # url(r'^foode/', include('foode.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
   #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

#urlpatterns += patterns('',
 #       url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
  #          'document_root': settings.MEDIA_ROOT,
   #         }),
    #)





