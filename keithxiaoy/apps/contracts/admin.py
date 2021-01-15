from django.contrib import admin
from import_export.admin import ImportExportMixin
from railguns.django.contrib.admin import SuperAdmin
from railguns.django.db.utils import get_object_or_none
from ..customers.models import Customer

from ..contracts.models import Contract, Buyer


class ContractAdmin(ImportExportMixin, SuperAdmin):
    list_display = ('id', 'number', 'valid_start_date', 'valid_end_date')
    search_fields = ('number',)
    filter_horizontal = ['buyers']


class BuyerAdmin(ImportExportMixin, SuperAdmin):
    list_display = ('id', 'get_customer', 'business_type', 'pre_pay_rate', 'trading_relate_amount')

    def get_customer(self, obj):
        customer_obj = get_object_or_none(Customer, using='default', pk=obj.customer_id)
        if customer_obj:
            return customer_obj.name
        return '未知'


admin.site.register(Contract, ContractAdmin)
admin.site.register(Buyer, BuyerAdmin)
