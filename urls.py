from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^gavbt/', include('gavbt.apps.foo.urls.foo')),

    # Uncomment this for admin:
     #(r'^admin/', include('django.contrib.admin.urls')),
     
	 # Main index
	 (r'^$', 'gavbt.main.views.index'),

	 # File directories
	 (r'^projects/(?P<path>.*)$', 'django.views.static.serve', 
		 {'document_root' : 'projects/', 'show_indexes': True}),

	 (r'^upload/(?P<path>.*)$', 'django.views.static.serve', 
		 {'document_root' : 'upload/', 'show_indexes': True})
)
