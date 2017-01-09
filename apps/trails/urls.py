from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^add$', views.add_state),
    url(r'^trips$', views.trips),
    url(r'^trail/add$', views.add_trips), 
    url(r'^trail/add/(?P<id>\d+)$', views.add_trips), 
   	url(r'^insert_trips$', views.insert_trips), 
   	url(r'^trail_info$', views.trail_info), 
  	
    url(r'^trail/create$', views.create), 
    url(r'^insert$', views.insert),
    url(r'^search$', views.search),
    url(r'^trails/(?P<id>\d+)$', views.trails_detail),
    url(r'^trail/join/(?P<id>\d+)$', views.join), 
    url(r'^trail/destination/(?P<id>\d+)$', views.user_destination),
    url(r'^logout$', views.logout),
    url(r'^trail/delete/(?P<id>\d+)$', views.delete),    
    url(r'^remove/(?P<trip_id>\d+)/(?P<id>\d+)$', views.remove_join),
	url(r'^process$', views.process),
	url(r'^process2$', views.process2)
]
