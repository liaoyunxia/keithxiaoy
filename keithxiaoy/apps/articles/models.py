# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from common.models import UserModel, TimeModel, StateModel, NoModel

ARTICLE_IMPORT_METHOD_CHOICES = ((0, ' 用户编辑'), (1, '爬虫获取'), (2, '用户复制'))
ARTICLE_TYPE_CHOICES = ((0, '草稿'), (1, '待审核'), (2, '过期'), (3, '显示'))


class Article(UserModel, TimeModel, StateModel, NoModel):
    url = models.CharField(_('url'), max_length=100, blank=True)
    import_method = models.IntegerField(_('import_method'), choices=ARTICLE_IMPORT_METHOD_CHOICES, default=0)
    name = models.CharField(_('name'), max_length=50)
    content = models.TextField(_('content'), blank=True)
    remark = models.CharField(_('remark'), max_length=200, blank=True)
    type = models.IntegerField(_('type'), choices=ARTICLE_TYPE_CHOICES, default=0)

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('article')