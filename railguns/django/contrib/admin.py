import locale

from django.contrib import admin, messages
from django.core import serializers
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from public.aliyun.aliyun_oss_url_sign import get_sign_url
from ...tools.utils import locale_currency
from ..db.models import OwnerModel


class PreviewMixin(object):
    image_width = 100
    image_height = 100

    def get_preview(self, obj):
        html = '<br>'.join('''<div style="width: {1}; height: {2}; overflow: hidden;">
                 <a href="{0}" rel="external" target="_blank">
                   <img src="{0}" max-width="{1}" max-height="{2} width="{1}" height="{2}">
                 </a>
               </div>'''.format(get_sign_url(item.strip()), self.image_width, self.image_height) for item in obj.images.split('\n'))
        return format_html(html)

    get_preview.short_description = _('preview')


class CurrencyMixin(object):

    def format_currency(self, amount, min, currency='IDR'):
        value = amount
        formatted = locale_currency(currency, value)
        if value < min:
            formatted = '<span style="color: red;"> {}</span>'.format(formatted)
        return format_html(formatted)

#
# class SuperAdmin(CurrencyMixin, PreviewMixin, admin.ModelAdmin):
#     readonly_fields = []  # 默认从tuple改为list
#
#     def get_readonly_fields(self, request, obj=None):
#         if obj:
#             return [f.name for f in obj._meta.get_fields() if not f.editable] + self.readonly_fields
#         return super().get_readonly_fields(request)
#
#     def get_sortable_by(self, request):
#         if self.readonly_fields and isinstance(self.readonly_fields, tuple):
#             messages.warning(request, 'readonly_fields 为 tuple, 建议改为 list, 修改页面未容错，会报错')
#         return super().get_sortable_by(request)
#
#     def save_model(self, request, obj, form, change):
#         if not obj.pk:  # 如果obj.pk不存在, 为新创建
#             if isinstance(obj, OwnerModel):
#                 obj.username = request.user.username
#                 obj.user_avatar = request.user.avatar
#         super().save_model(request, obj, form, change)
#
#     def log_change(self, request, obj, message):
#         new_message = 'json: {}'.format(serializers.serialize('json', [obj]))
#         super().log_change(request, obj, new_message)
