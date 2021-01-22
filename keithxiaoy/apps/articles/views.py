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
from ..articles.models import Article


@permission_classes([AllowAny])
class ArticleDetail(WebView):

    def get(self, request, *args, **kwargs):

        article_name = kwargs.get('title') if kwargs.get('title') else 'about_me'

        # if not request.user.is_authenticated():
        #     return redirect('/accounts/login/')
        article_obj = Article.objects.get(english_name=article_name)
        article_data = {'name': article_obj.name, 'content': article_obj.content}
        title = kwargs.get('title', '{}'.format(article_name))
        # opt_type = self.request.GET.get('type', '')
        # endpoint = '{}{}'.format('/api/v1/orders', request.get_full_path())
        # template_name = self.template_nam
        template_name = 'entry.html'
        return render(request, template_name, locals())