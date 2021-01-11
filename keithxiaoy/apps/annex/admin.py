from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from import_export.admin import ImportExportMixin
from railguns.django.contrib.admin import SuperAdmin

from .models import AnnexTemplate


class AnnexTemplateAdminForm(forms.ModelForm):
    content = forms.CharField(label=_('content'), widget=CKEditorWidget())

    class Meta:
        model = AnnexTemplate
        fields = '__all__'


class AnnexTemplateAdmin(ImportExportMixin, SuperAdmin):
    list_display = ('id', 'name', 'type')
    search_fields = ('name',)
    form = AnnexTemplateAdminForm


admin.site.register(AnnexTemplate, AnnexTemplateAdmin)
