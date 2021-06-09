# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import datetime
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db import models
from mdeditor.fields import MDTextField
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from railguns.django.db.models import BaseModel
from ..products.models import Product
from ..common.models import UserModel, TimeModel, StateModel, NoModel

ORDER_STATUS_CHOICES = ((-1, '取消/关闭'), (0, '创建'), (1, '待支付'), (2, '支付成功'), (3, '已发货'))

ARTICLE_TYPE_CHOICES = ((0, '草稿'), (1, '待审核'), (2, '过期'), (3, '显示'))
ARTICLE_CATEGORY_CHOICES = ((0, '文章'), (1, '视频'), (2, '想法'), (3, '其他'))

PAY_TYPE_CHOICES = ((0, '现金'), (1, '银行转账'), (2, '微信'), (3, '支付宝'))


class GoodsSale(BaseModel, UserModel, TimeModel):
    '''
    每个产品的销售记录
    '''
    #
    product = models.ForeignKey(Product, verbose_name=_('goods'), blank=False)
    #
    count = models.IntegerField(_('count'), default=0)
    # 单件售价
    out_price = models.FloatField('out_price', default=0)
    # 出售总价
    out_amount = models.FloatField('out_amount', default=0)
    #
    remark = models.CharField(_('remark'), max_length=200, blank=True)

    class Meta:
        verbose_name = _('goods_sale')
        verbose_name_plural = _('goods_sale')


class Order(BaseModel, UserModel, TimeModel, StateModel, NoModel):
    # 订单
    customer_name = models.CharField(_('customer_name'), max_length=50)
    customer_address = models.CharField(_('customer_address'), max_length=50)
    customer_phonenumber = models.CharField(_('customer_phonenumber'), max_length=50)
    pay_method = models.PositiveIntegerField(_('pay_method'), choices=PAY_TYPE_CHOICES, default=0)
    # 对应商品
    goods = models.ManyToManyField(GoodsSale, verbose_name=_('goods'), blank=True)

    price = models.BooleanField(_('price'), default=False)
    discount = models.FloatField(_('discount'), default=1)

    remark = models.CharField(_('remark'), max_length=200, blank=True)
    status = models.IntegerField(_('status'), choices=ORDER_STATUS_CHOICES, default=0)
    is_active = models.BooleanField(_('is_active'), default=True)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('order')



