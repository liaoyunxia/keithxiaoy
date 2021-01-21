# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.models import User
# Create your models here.


class TimeModel(models.Model):
    '''
    class: 包含创建和修改时间的基础类
    '''

    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=u'创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name=u'更新时间')

    class Meta:
        abstract = True


class NoModel(models.Model):
    '''
    class: 包含唯一编号的基础类
    '''
    no = models.CharField(max_length=32, unique=True, verbose_name=u'编号')

    class Meta:
        abstract = True


class UserModel(models.Model):
    user = models.ForeignKey(User, verbose_name=u'创建者')

    class Meta:
        abstract = True


STATE_TYPE_CHOICES = ((0, '正常'), (1, '临时'), (-1, '删除'))


class StateModel(models.Model):
     state = models.IntegerField(_('state'), choices=STATE_TYPE_CHOICES, default=1)

     class Meta:
         abstract = True