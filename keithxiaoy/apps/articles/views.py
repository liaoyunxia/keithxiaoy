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
class ArticleDetail(WebView):

    def get(self, request, *args, **kwargs):
        import markdown
        dj_logger.info('kwargs={} ; '.format(kwargs))

        article_name = kwargs.get('title') if kwargs.get('title') else 'about_me'

        # if not request.user.is_authenticated():
        #     return redirect('/accounts/login/')
        article_obj = Article.objects.get(english_name=article_name)

        if article_obj.import_method == 1:
            dj_logger.info('do1  ')
            return redirect(article_obj.url)

        article_data = article_obj
        article_detail = markdown.markdown(article_obj.md_content)
        title = kwargs.get('title', '{}'.format(article_name))
        # opt_type = self.request.GET.get('type', '')
        # endpoint = '{}{}'.format('/api/v1/orders', request.get_full_path())
        # template_name = self.template_nam
        template_name = 'article_detail.html'
        return render(request, template_name, locals())


# Create your views here.
def uploadImg(request):
    if request.method == "POST":
        file = request.FILES.get('img')
        md5=GetFileMd5(file)
        imgobj = UploadImage.objects.filter(imgMd5=md5)
        if not imgobj:
            size = file.size
            if not FileSize(size):
                info = {'code': 403, 'error': '文件太大!'}
                return JsonResponse(info)
            ext = os.path.splitext(file.name)[1]
            if not JudgeType(ext):
                info = {'code': 403, 'error': '文件类型错误！'}
                return JsonResponse(info)
            path = Rename(file)
            name = os.path.basename(path)
            create=UploadImage.objects.create(imgName=name, imgMd5=md5,imgType=ext,imgSize=size,imgPath=path)
            url='http://'+settings.HOST_NAME +"/"+create.imgPath
            info={'code':200,'imgurl':url}
            return JsonResponse(info)
        else:
            url ='http://'+settings.HOST_NAME +"/"+imgobj.first().imgPath
            info = {'code': 200, 'imgurl': url}
            return JsonResponse(info)

