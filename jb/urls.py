from django.conf.urls import url

from . import views

app_name = 'jb'

urlpatterns = [
	#ex: /jb/
	url(r'^$', views.AllBunksView.as_view(), name='index'),
	#ex: /jb/1
	url(r'^(?P<user_id>[0-9]+)/$', views.personalBunksView, name='personalBunksView'),
	#ex: /jb/1/bunk
	url(r'^(?P<user_id>[0-9]+)/bunk/$', views.bunk, name='bunk'),
]