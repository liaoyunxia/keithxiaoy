# -*- coding: utf-8 -*-
"""firstsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:

Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^xiaohege/$', views.TrourismHome.as_view()),
    url(r'^contact/$', views.ConnectsUs.as_view()),
    url(r'^about-us/$', views.AbountUs.as_view()),
    url(r'^tours/$', views.Tours.as_view()),
    url(r'^blog/$', views.Blog.as_view()),
    url(r'^login/$', views.Login.as_view()),
    url(r'^regsiter/$', views.Register.as_view()),
    url(r'^booking/$', views.Booking.as_view()),
    url(r'^team/$', views.Team.as_view()),
    url(r'^faq/$', views.Faq.as_view()),
    url(r'^destination/$', views.Destination.as_view()),
    url(r'^destination-detail/$', views.DestinationDetail.as_view()),

]
