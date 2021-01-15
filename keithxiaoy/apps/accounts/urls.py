from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^update_password/$', views.update_password),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout, name='logout'),
]
