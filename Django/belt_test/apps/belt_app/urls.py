from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^home$', views.home),
    url(r'^logout$', views.logout),
    url(r'^info/(?P<id>\d+)$', views.info),
    url(r'^add/(?P<id>\d+)$', views.add),
    url(r'^remove/(?P<id>\d+)$', views.remove),

]
