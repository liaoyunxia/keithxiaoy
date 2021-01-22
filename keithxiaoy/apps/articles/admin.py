# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib import admin, auth
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
# from import_export.admin import ImportExportMixin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    image_width = 32
    image_height = 32

    fieldsets = (
        (None, {'fields': ('name', 'no', 'english_name')}),
        (_('article content'), {'fields': ('remark', 'url', 'content')}),
        (_('article state'), {'fields': ('type', 'state', 'import_method', 'user')}),
        # (_('time'), {'fields': ('modify_time',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('name', 'no', 'english_name')}),
        (_('article content'), {'fields': ('remark', 'url', 'content')}),
        (_('article state'), {'fields': ('type', 'state', 'import_method', 'user')}),
    )

    list_display = ['id', 'name', 'english_name','type', 'import_method', 'url', 'remark','user', 'state','modify_time']
    list_filter = ['import_method', 'user', 'state', 'type']
    suit_list_filter_horizontal = ['import_method', 'name', 'state']
    search_fields = ['name', 'user__username']


admin.site.register(Article, ArticleAdmin)