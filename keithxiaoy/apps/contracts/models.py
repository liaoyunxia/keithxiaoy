from django.db import models
import django.utils
from django.utils.translation import ugettext_lazy as _
from railguns.django.db.models import OwnerModel
from railguns.django.db.utils import get_object_or_none


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

