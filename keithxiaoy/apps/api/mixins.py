from collections import OrderedDict

from django.contrib.auth import get_user_model
from railguns.django.db.utils import get_object_or_none
from rest_framework import serializers

from public.utils.active_code import Active_code
from public.utils.func_ext import get_nickname, get_username

from ..accounts.models import USER_TYPE_CHOICES


class CardIdStrMixin(serializers.Serializer):
    card_id_str = serializers.SerializerMethodField()

    def get_card_id_str(self, obj):
        return str(obj.card_id)


class UserMixin(serializers.Serializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user_obj = get_object_or_none(get_user_model(), using='default', pk=obj.user_id)
        data = []
        if user_obj:
            data = [{'url': item.strip(), 'uri': item.strip()} for item in obj.user_image_urls.split('\n')]
        return OrderedDict([
            ('id', user_obj.id if user_obj else 0),
            ('username', user_obj.username if user_obj else ''),
            ('name', user_obj.name if user_obj else ''),
            ('images', OrderedDict([('count', len(data)), ('next', None), ('previous', None), ('results', data)]))
        ])


class UserOrderMixins(serializers.Serializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        data = [{'url': item.strip(), 'uri': item.strip()} for item in obj.image_urls.split('\n')]
        return OrderedDict([
            ('id', obj.user_id),
            ('nickname', get_nickname(obj.nickname)),
            ('username', get_username(obj.username)),
            ('images', OrderedDict([('count', len(data)), ('next', None), ('previous', None), ('results', data)]))
        ])


class PromotionCodeMixin(serializers.Serializer):
    promotion_code = serializers.SerializerMethodField()

    def get_promotion_code(self, obj):
        return Active_code().encode(obj.id)


class IdCardNumberNameMixin(serializers.Serializer):
    id_card_number = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_id_card_number(self, obj):
        temp_list = []
        if len(obj.id_card_number) != 0:
            for x in range(len(obj.id_card_number) - 7):
                temp_list.append('*')
            return obj.id_card_number[:3] + ''.join(temp_list) + obj.id_card_number[-4:]
        return obj.id_card_number

    def get_name(self, obj):
        temp_list = []
        if len(obj.name) != 0:
            for x in range(len(obj.name) - 1):
                temp_list.append('*')
            return ''.join(temp_list) + obj.name[-1:]
        return obj.name


class UserTypeMixin(serializers.Serializer):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        type_list = [i[1] for i in USER_TYPE_CHOICES if i[0] == obj.type]
        if len(type_list) != 0:
            return {'code': obj.type, 'message': type_list[0]}
        else:
            return {'code': 0, 'message': ''}
