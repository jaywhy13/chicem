from django.conf.urls.defaults import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^data/(\w*)$',views.data, name='data'),
    url(r'^search/(.*)$', views.search, name='search'),
    url(r'^sections$', views.sections, name='sections'),
    url(r'^sections_coords$', views.sections_coords, name='sections_coords'),

)
