from django.db import models
from django.utils.translation import ugettext_lazy as _
from railguns.django.db.models import OwnerModel

ANNEX_TYPE = ((1, '发票签收单'), (2, '利息表'), (3, '内部核票'), (4, '保理合同'), (5, '咨询服务合同'),
              (6, '商业汇票贴现总协议'), (7, '贴现凭证'), (8, '业务审查表'), (9, '业务审批表'), (10, '用款申请单'),
              (11, '应收款转让清单'), (12, '应收款登记协议'), (13, '有追索权国内保理合同'))


class AnnexTemplate(OwnerModel):
    """附件"""
    name = models.CharField(_('name'), max_length=100, blank=True)
    type = models.PositiveSmallIntegerField(_('type'), choices=ANNEX_TYPE, default=1)
    content = models.TextField(_('content'), blank=True)
    remark = models.CharField(_('remark'), max_length=1000, blank=True)

    class Meta(OwnerModel.Meta):
        verbose_name = _('附件模版')
        verbose_name_plural = _('附件模版')

    def __str__(self):
        return self.name


class Annex(models.Model):
    bill_id = models.IntegerField(_('票据单号'), unique=True)
    discount_agreement = models.CharField(_('贴现总协议'), max_length=200, default='', blank=True)
    invoice_sign = models.CharField(_('发票签收单'), max_length=200, default='', blank=True)
    payment_requisition = models.CharField(_('用款申请单'), max_length=200, default='', blank=True)
    factor_contract = models.CharField(_('保理合同'), max_length=200, default='', blank=True)
    investigate_table = models.CharField(_('业务审查表'), max_length=200, default='', blank=True)
    approve_table = models.CharField(_('业务审批表'), max_length=200, default='', blank=True)
    discounting_voucher = models.CharField(_('贴现凭证'), max_length=200, default='', blank=True)
    interest_table = models.CharField(_('利息表'), max_length=200, default='', blank=True)
    ticket_file = models.CharField(_('核票文件'), max_length=200, default='', blank=True)
    collection_agreement = models.CharField(_('咨询服务合同'), max_length=200, default='', blank=True)
    receivable_inventory = models.CharField(_('应收账款转让清单'), max_length=200, default='', blank=True)
    receivable_registration_agreement = models.CharField(_('应收款登记协议'), max_length=200, default='', blank=True)
    other_files = models.CharField(_('其他文件'), max_length=200, default='', blank=True)

    class Meta(OwnerModel.Meta):
        verbose_name = _('附件')
        verbose_name_plural = _('附件')
