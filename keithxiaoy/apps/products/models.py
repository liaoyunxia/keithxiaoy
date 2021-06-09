# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import datetime
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db import models
from mdeditor.fields import MDTextField
from railguns.django.db.models import BaseModel
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from ..common.models import UserModel, TimeModel, StateModel, NoModel

UNIT_CHOICES = ((0, '个'), (1, '颗'), (2, '件'), (3, '条/根'), (4, '米'), (5, '快'), (6, '只'))
PRODUCT_TYPE = ((0, '膨胀壶'), (1, '门锁'))
PRODUCT_SUB_TYPE = ((0, '膨胀壶'), (1, '门锁'))
PRODUCT_IO_TYPE = ((0, '入库'), (1, '出库'))


class Product(BaseModel, UserModel, TimeModel, StateModel, NoModel):
    # 名称
    name = models.CharField(_('name'), max_length=50)
    english_name = models.CharField(_('english_name'), max_length=50)
    # 编码
    sku = models.CharField(_('sku'), unique=True, max_length=50)
    # 型号
    version = models.CharField('version', max_length=50, blank=True)
    # 厂家
    factory = models.CharField('factory', max_length=50, blank=True)
    unit = models.CharField('unit', choices=UNIT_CHOICES, default=0)
    # 销售价
    sale_price = models.FloatField('sale_price', default=0)
    # 匹配车型
    match_car = models.CharField(_('match_car'), max_length=150)
    # 出售折扣
    discount = models.FloatField(_('discount'), default=1)
    # 分类
    type = models.PositiveIntegerField(_('type'), choices=PRODUCT_TYPE, default=0)
    sub_type = models.PositiveIntegerField(_('sub_type'), choices=PRODUCT_SUB_TYPE, default=0)
    # 标签
    tags = models.CharField(_('tags'), max_length=200, blank=True)
    # 产品描述
    detail = models.CharField(_('detail'), max_length=200, blank=True)
    # 备份
    remark = models.CharField(_('remark'), max_length=200, blank=True)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('product')


class Purchase(BaseModel, UserModel, TimeModel):
    '''
    采购记录
    '''
    #
    product = models.ForeignKey(Product, verbose_name=_('goods'), blank=False)
    #
    count = models.IntegerField(_('count'), default=0)
    # 进货价
    in_price = models.FloatField('in_price', default=0)
    # 总价
    in_amount = models.FloatField('in_amount', default=0)
    # 入库时间
    inbound_time = models.DateTimeField('inbound_time', auto_now_add=True)
    #
    remark = models.CharField(_('remark'), max_length=200, blank=True)

    class Meta:
        verbose_name = _('purchase')
        verbose_name_plural = _('purchase')
