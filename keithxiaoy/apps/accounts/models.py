import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from ..organizations.models import Organization


class UserManager(BaseUserManager):
    # https://docs.djangoproject.com/en/dev/topics/auth/customizing/#a-full-example
    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)


GENDER_CHOICES = (('m', _('male')), ('f', _('female')), ('', '未填写'))
USER_TYPE_CHOICES = ((0, '普通帐户'), (1, '企业帐户'), (2, '企业员工'))


class User(AbstractUser):
    nickname = models.CharField(_('nickname'), max_length=30)
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES, blank=True)
    name = models.CharField(_('full_name'), max_length=30, blank=True)
    about = models.CharField(_('about'), max_length=70, blank=True)
    image_urls = models.CharField(_('image_urls'), max_length=2000, blank=True)
    tags = models.CharField(_('tags'), max_length=200, blank=True)
    id_card_number = models.CharField(_('id_card_number'), max_length=18, blank=True)
    phone_number = models.CharField(_('phone_number'), max_length=20, blank=True)
    social_user_id = models.CharField(_('social_user_id'), max_length=30, blank=True)
    social_site = models.CharField(_('social_site'), max_length=2, choices=(('wb', 'wb'), ('tw', 'tw'), ('fb', 'fb'), ('wx', 'wx')), default='wx', blank=True)
    risk_level = models.PositiveSmallIntegerField(_('risk_level'), default=60)
    level = models.PositiveIntegerField(_('level'), default=1)
    grade = models.PositiveSmallIntegerField(_('grade'), default=0)
    birthday = models.DateTimeField(_('birthday'), default=datetime.datetime(1980, 1, 1, 12, 0, 0), editable=False)  # 生日.
    organization = models.ManyToManyField(Organization, blank=True)
    type = models.PositiveSmallIntegerField(_('type'), choices=USER_TYPE_CHOICES, default=0)
    is_login = models.BooleanField(_('is_login'), default=False)
    objects = UserManager()
    REQUIRED_FIELDS = ['nickname', 'email']  # 只在createsuperuser时起作用

    def clean(self, *args, **kwargs):
        if self.id_card_number and self.id_card_number != '':
            if get_user_model().objects.filter(id_card_number=self.id_card_number.upper()).exclude(id=self.pk):
                raise ValidationError('身份证已经绑定')
        super(User, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.id_card_number:
            self.id_card_number = self.id_card_number.upper()
        super(User, self).save(*args, **kwargs)


class BaseUid(models.Model):
    user_id = models.IntegerField()
    social_user_id = models.CharField(primary_key=True, max_length=30, editable=False)
    is_active = models.BooleanField(_('active'), default=True)  # TODO: 有什么作用?

    class Meta:
        abstract = True


class WBUid(BaseUid):
    class Meta:
        db_table = 'social_wb'


class WXUid(BaseUid):
    class Meta:
        db_table = 'social_wx'


class TWUid(BaseUid):
    class Meta:
        db_table = 'social_tw'


class FBUid(BaseUid):
    class Meta:
        db_table = 'social_fb'
