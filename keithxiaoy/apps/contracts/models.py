from django.db import models
import django.utils
from django.utils.translation import ugettext_lazy as _
from railguns.django.db.models import OwnerModel
from railguns.django.db.utils import get_object_or_none

from ..customers.models import Customer


class BuyerManager(models.Manager):
    # https://docs.djangoproject.com/en/dev/topics/auth/customizing/#a-full-example
    def _create_buyer(self, request, **extra_fields):
        obj = self.model(**extra_fields)
        obj.user_id = request.user.id
        obj.username = request.user.username
        obj.user_image_urls = request.user.image_urls
        obj.save(using=self._db)
        obj.save()
        return obj

    def create_buyer(self, request, **extra_fields):
        return self._create_buyer(request, **extra_fields)


class Contract(OwnerModel):
    number = models.CharField(_('保理号'), max_length=100)
    seller_id = models.IntegerField(_('卖方'), default=0)
    valid_start_date = models.DateTimeField(_('生效日'), default=django.utils.timezone.now, help_text='生效日')
    valid_end_date = models.DateTimeField(_('截止日'), default=django.utils.timezone.now, help_text='截止日')
    pre_pay_max_x = models.BigIntegerField(_('保理预付款最高金额(小写)'), default=0)
    pre_pay_max_d = models.CharField(_('保理预付款最高金额(大写)'), max_length=100, blank=True)
    penalty_interest = models.IntegerField(_('逾期罚息上浮'), default=0)
    sign_date = models.DateTimeField(_('签约日'), default=django.utils.timezone.now, help_text='签约日')
    sign_address = models.CharField(_('签约地点'), max_length=200, blank=True)
    buyers = models.ManyToManyField(Buyer, verbose_name=_('买方信息'), blank=True)
    url = models.CharField(_('url'), max_length=200, blank=True)

    def __str__(self):
        return self.number
