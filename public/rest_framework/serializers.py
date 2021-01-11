from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler


class UserCreatedSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    is_manager = serializers.SerializerMethodField()
    is_financier = serializers.SerializerMethodField()
    is_first_login = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        exclude = ('password', 'is_superuser', 'is_staff', 'date_joined', 'groups', 'user_permissions', 'is_active', 'last_login')

    def get_is_first_login(self, obj):
        if obj.is_login:
            return 0
        return 1

    def get_token(self, obj):
        return jwt_encode_handler(jwt_payload_handler(obj))

    def get_type(self, obj):
        USER_TYPE_CHOICES = ((0, '普通帐户'), (1, '企业帐户'), (2, '企业员工'))
        type_list = [i[1] for i in USER_TYPE_CHOICES if i[0] == obj.type]
        if len(type_list) != 0:
            return {'code': obj.type, 'message': type_list[0]}
        else:
            return {'code': 0, 'message': ''}

    def get_is_manager(self, obj):
        group_name = [item.name for item in obj.groups.all()]
        if '客户经理' in group_name:
            return 1
        else:
            return 0

    def get_is_financier(self, obj):
        group_name = [item.name for item in obj.groups.all()]
        if '转贴人员' in group_name:
            return 1
        else:
            return 0
