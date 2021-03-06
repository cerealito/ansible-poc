from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.http import HttpResponseRedirect

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'monitoring.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', lambda r: HttpResponseRedirect('charts/')),
    url(r'^charts/', include('charts.urls', namespace='charts')),
    url(r'^admin/', include(admin.site.urls)),
)
