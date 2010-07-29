from django.conf.urls.defaults import *

urlpatterns = patterns('',
        # Example:
        # (r'^gbtdotnet/', include('gbtdotnet.apps.foo.urls.foo')),

        # Uncomment this for admin:
        #(r'^admin/', include('django.contrib.admin.urls')),

        # Main index
        (r'^$', 'gbtdotnet.main.views.index'),

        (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
            {'document_root' : 'media/', 'show_indexes': True}),

        (r'^projects/(?P<path>.*)$', 'django.views.static.serve', 
            {'document_root' : 'projects/', 'show_indexes': True}),

        (r'^upload/(?P<path>.*)$', 'django.views.static.serve', 
            {'document_root' : 'upload/', 'show_indexes': True})
        )
