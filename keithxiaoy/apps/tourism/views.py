# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import copy
import datetime
import json
import logging
from datetime import timedelta
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
# from rest_framework import status
from rest_framework.decorators import permission_classes
# from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from railguns.django.generics import WebView
from ..articles.models import Article, UploadImage
from ..articles.tools import *

from django.conf import settings
dj_logger = logging.getLogger('django')


@permission_classes([AllowAny])
class TrourismHome(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'tourism-index.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class Blog(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'blog.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class ConnectsUs(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'contact.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class Tours(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'tours.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class AbountUs(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'about-us.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class Register(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'register.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class Faq(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'faq.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class Login(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'login.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class DestinationDetail(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'destination-details.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class Destination(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'destinations.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class Booking(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'booking.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class Team(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'team.html'
        return render(request, template_name, locals())



