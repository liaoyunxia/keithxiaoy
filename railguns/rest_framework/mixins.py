import datetime

from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import make_password
from django.utils.timezone import localtime
from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import Serializer
from rest_framework_jwt.settings import api_settings

from .utils import get_nested_list


class PasswordMixin(Serializer):
    password = CharField(style={'input_type': 'password'}, min_length=6, max_length=128, write_only=True)

    # SO: https://stackoverflow.com/questions/29746584/django-rest-framework-create-user-with-password
    def validate_password(self, value):
        return make_password(value)


class TokenMixin(Serializer):
    token = SerializerMethodField()

    def get_token(self, obj):
        request = self.context.get('request')
        if request:
            auth_login(request, obj)  # 主要为了记录last_login的, 其他的作用待研究
        else:
            print('request is None, 请在代码手动传入, 否则无法自动登录')
        # https://getblimp.github.io/django-rest-framework-jwt/#additional-settings
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        return jwt_encode_handler(jwt_payload_handler(obj))


class ModelMixin(object):

    def get_model(self):
        return self.serializer_class.Meta.model


class ImagesMixin(Serializer):
    images = SerializerMethodField()

    def get_images(self, obj):
        if hasattr(obj, 'images'):
            return get_nested_list([{'uri': item.strip()} for item in obj.images.split('\n') if item.strip()])
        else:
            return '👈⚠️️字段不存在，请去除。'


class TagsMixin(Serializer):
    tags = SerializerMethodField()

    def get_tags(self, obj):
        if hasattr(obj, 'tags'):
            return [item.strip() for item in obj.tags.split('#') if item.strip()]
        else:
            return '👈⚠️️字段不存在，请去除。'


class OwnerMixin(object):

    def pre_save(self, obj):
        obj.user_id = self.request.user.id


class StartDateMixin(Serializer):
    start_date = SerializerMethodField()

    def get_start_date(self, obj):
        return localtime(obj.start_time).strftime('%Y-%m-%d')


class EndDateMixin(Serializer):
    end_date = SerializerMethodField()

    def get_end_date(self, obj):
        if obj.period <= 0:
            return ''
        else:
            return self.get_date_after_period(localtime(obj.start_time), obj.period)

    def get_date_after_period(self, date, period):
        days = period
        if period >= 0:
            days = period - 1
        date_time = date + datetime.timedelta(days=days)
        return date_time.strftime('%Y-%m-%d')