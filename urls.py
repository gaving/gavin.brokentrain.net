from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^gavbt/', include('gavbt.apps.foo.urls.foo')),

    # Uncomment this for admin:
     #(r'^admin/', include('django.contrib.admin.urls')),
     
	 # Main index
	 (r'^$', 'gavbt.main.views.index'),
)
