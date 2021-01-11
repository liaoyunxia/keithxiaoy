from django.db import models
from django.utils.translation import ugettext_lazy as _
from railguns.cloudfile.fields import CloudFileField


class File(models.Model):
    url = CloudFileField()
    name = models.CharField(_('名称'), max_length=100, blank=True)
    type = models.CharField(_('type'), max_length=100, choices=(('1', '图片'), ('2', 'HTML页面'), ('3', 'js'), ('4', 'css'), ('5', '其他')), blank=True)

    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')
