from django.conf.urls import url

from . import views

app_name = 'jb'

urlpatterns = [
	#ex: /jb/
	url(r'^$', views.AllBunksView.as_view(), name='index'),
	#ex: /jb/signup
	url(r'^signup/$', views.signup, name='signup'),
	#ex: /jb/1
	url(r'^(?P<username>\w+)/$', views.personalBunksView, name='personalBunksView'),
	#ex: /jb/1/bunk
	url(r'^(?P<username>\w+)/bunk/$', views.bunk, name='bunk'),

]