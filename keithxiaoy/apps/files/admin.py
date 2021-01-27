from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from railguns.django.contrib.admin import SuperAdmin

from .models import File


class FileAdmin(SuperAdmin):
    list_display = ('id', 'type', 'name', 'get_preview', 'url')
    search_fields = ('url', 'name',)
    filter_list = ('type',)

    def get_preview(self, obj):
        return format_html('<a href="{0}" rel="external"><img src="/media{0}" width="50" height="50"/></a>'.format(obj.url))
    get_preview.short_description = _('preview')

admin.site.register(File, FileAdmin)
