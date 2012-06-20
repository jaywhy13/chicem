from django.conf.urls.defaults import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^data/(\w*)$',views.data, name='data'),
    url(r'^search/(.+)', views.search, name='search'),
)
