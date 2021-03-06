# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import datetime
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db import models
from mdeditor.fields import MDTextField
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from ..common.models import UserModel, TimeModel, StateModel, NoModel

ARTICLE_IMPORT_METHOD_CHOICES = ((0, ' 用户编辑'), (1, '爬虫获取'), (2, '用户复制'))
ARTICLE_TYPE_CHOICES = ((0, '草稿'), (1, '待审核'), (2, '过期'), (3, '显示'))
ARTICLE_CATEGORY_CHOICES = ((0, '文章'), (1, '视频'), (2, '想法'), (3, '其他'))


class Article(UserModel, TimeModel, StateModel, NoModel):
    url = models.CharField(_('url'), max_length=100, blank=True)
    import_method = models.IntegerField(_('import_method'), choices=ARTICLE_IMPORT_METHOD_CHOICES, default=0)
    name = models.CharField(_('name'), max_length=50)

    english_name = models.CharField(_('english_name'), max_length=50)
    summary = models.TextField(_('summary'), blank=True)
    # preview = models.CharField(_('preview'), max_length=500, blank=True, default='', help_text='预览图')
    images = models.CharField(_('images'), max_length=500, blank=True, default='',  help_text='涉及的图')
    set_top = models.BooleanField(_('set_top'), default=False)
    priority = models.IntegerField(_('priority'), default=0, help_text='越小优先级越高')
    category = models.IntegerField(_('category'), choices=ARTICLE_CATEGORY_CHOICES, default=0)

    content = RichTextField(_('content'), blank=True, help_text='first show')
    remark = models.CharField(_('remark'), max_length=200, blank=True)
    type = models.IntegerField(_('type'), choices=ARTICLE_TYPE_CHOICES, default=0)
    bg_img = models.ImageField(upload_to='article_bg_img', verbose_name='图片', null=True)
    md_content = MDTextField(blank=True, help_text='show when content is null')

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('article')


class UploadImage(TimeModel):
    imgName = models.CharField(max_length=252, default="", verbose_name="文件名")
    imgMd5 = models.CharField(max_length=128, verbose_name="MD5值")
    imgType = models.CharField(max_length=32, verbose_name="类型")
    imgSize = models.IntegerField(verbose_name="大小")
    imgPath = models.CharField(max_length=128, verbose_name="图片路径")
    content = MDTextField()

    # imgUpdated = models.CharField(max_length=64,default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),verbose_name="更新时间")

    def __str__(self):
        return self.imgName

    class Meta:
        db_table = 'upload_image'


