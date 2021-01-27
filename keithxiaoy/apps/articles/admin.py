# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.html import format_html
from django.contrib import admin
from django.contrib import admin, auth
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
# from import_export.admin import ImportExportMixin

from .models import Article, UploadImage


class ArticleAdmin(admin.ModelAdmin):
    image_width = 32
    image_height = 32

    fieldsets = (
        (None, {'fields': ('name', 'no', 'english_name', 'bg_img','priority', 'category', 'set_top')}),
        (_('article content'), {'fields': ('remark', 'url', 'summary', 'content')}),
        (_('article state'), {'fields': ('type', 'state', 'import_method', 'user')}),
        # (_('time'), {'fields': ('modify_time',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('name', 'no', 'english_name', 'bg_img', 'priority', 'category', 'set_top')}),
        (_('article content'), {'fields': ('remark', 'url', 'summary', 'content', )}),
        (_('article state'), {'fields': ('type', 'state', 'import_method', 'user')}),
    )

    list_display = ['id', 'priority', 'get_preview', 'name', 'english_name', 'category', 'type', 'import_method', 'url', 'remark','user', 'state','modify_time']
    list_filter = ['import_method', 'user', 'state', 'type', 'category', ]
    suit_list_filter_horizontal = ['import_method', 'name', 'state']
    search_fields = ['name', 'user__username', 'url', 'english_name']

    def get_preview(self, obj):
        return format_html('<a href="{0}" rel="external"><img src="/media{0}" width="50" height="50"/></a>'.format(obj.bg_img))
    get_preview.short_description = _('preview')


class UploadImageAdmin(admin.ModelAdmin):
    list_display = ['imgName', 'imgType', 'imgSize', 'imgPath']
    list_filter = ['imgType']
    search_fields = ['imgName']


admin.site.register(Article, ArticleAdmin)
admin.site.register(UploadImage, UploadImageAdmin)