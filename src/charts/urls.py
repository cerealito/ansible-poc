from django.conf.urls import patterns, url

from charts import views

urlpatterns = patterns('',
                       # root of charts/
                       url(r'^$', views.index, name='index'),
                       #
                       url(r'^(?P<host_id>\d+)/', views.host_resources, name='host_url')
                       )
