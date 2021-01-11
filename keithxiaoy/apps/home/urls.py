from django.conf.urls import url
from railguns.django.generics import WebView
from . import views


urlpatterns = [
    url(r'^$', views.HomeView.as_view(name='home'), {'title': '首页', 'child_header': 1}),
    url(r'^caculater/$', views.caculater),
    url(r'^users/(?P<pk>[0-9]+)/notifications/$', WebView.as_view(name='message'), {'title': '消息列表'}),
    url(r'^wx_redirect/$', views.wx_redirect_url)
]
