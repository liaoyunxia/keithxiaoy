# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib import admin, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import ugettext_lazy as _
# from import_export.admin import ImportExportMixin

from articles.models import Article


class ArticleAdmin(admin.ModelAdmin):
    image_width = 32
    image_height = 32

    fieldsets = (
        (None, {'fields': ('name', 'no')}),
        (_('article content'), {'fields': ('remark', 'url', 'content')}),
        (_('article state'), {'fields': ('type', 'state', 'import_method', 'user')}),
        # (_('time'), {'fields': ('modify_time',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('name', 'no')}),
        (_('article content'), {'fields': ('remark', 'url', 'content')}),
        (_('article state'), {'fields': ('type', 'state', 'import_method', 'user')}),
    )

    list_display = ['id', 'name', 'type', 'import_method', 'remark', 'user', 'state','modify_time']
    list_filter = ['import_method', 'user', 'state', 'type']
    suit_list_filter_horizontal = ['import_method', 'name', 'state']
    search_fields = ['name', 'user__username']
    # filter_horizontal = ('groups', 'user_permissions', )


admin.site.register(Article, ArticleAdmin)