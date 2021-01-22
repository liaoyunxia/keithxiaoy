from django.contrib import admin, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import ugettext_lazy as _
from railguns.django.contrib.admin import SuperAdmin
from .models import WXUid
from import_export.admin import ImportExportMixin


class UserAdmin(ImportExportMixin, auth.admin.UserAdmin):  # TODO: 用户导入功能太危险, 可以轻松导入管理员.
    image_width = 32
    image_height = 32

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('nickname', 'gender', 'image_urls', 'about', 'tags')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'date_joined', 'name', 'email', 'phone_number', 'id_card_number', 'social_user_id',)}),
        (_('Permissions'), {'fields': ('type', 'is_active', 'is_staff', 'groups',)}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('username', 'password1', 'password2')}),
        (None, {'classes': ('wide',),
                'fields': ('nickname', 'gender', 'image_urls')})
    )
    form = UserChangeForm
    list_display = ['id', 'username', 'get_groups', 'phone_number', 'date_joined', 'is_active']
    list_filter = ['is_staff', 'gender', 'username', 'is_active']
    suit_list_filter_horizontal = ['gender', 'username', 'is_active']
    search_fields = ['username', 'id', 'first_name', 'last_name', 'email', 'name']
    filter_horizontal = ('groups', 'user_permissions')

    def get_groups(self, obj):
        return '#'.join([item.name for item in obj.groups.all()])

    def has_delete_permission(self, request, obj=None):
        return request.user.username == 'admin'

    def get_actions(self, request):  # 移除delete菜单
        actions = super(UserAdmin, self).get_actions(request)
        if not self.has_delete_permission(request):
            del actions['delete_selected']
        return actions

    def get_readonly_fields(self, request, obj):
        if obj:
            if not request.user.is_superuser:
                fields = [f.name for f in obj._meta.get_fields()]
                if request.user.type == 1:
                    fields.remove('is_active')
                if request.user.id == obj.id:  # 自己和admin才能改自己密码.
                    fields.remove('password')
                return fields
            else:
                return ('risk_level', 'level', 'grade')
        return super(UserAdmin, self).get_readonly_fields(request)


class WeiBoAdmin(SuperAdmin):
    list_display = ('social_user_id', 'user_id')
    search_fields = ('user_id', 'social_user_id')


admin.site.register(get_user_model(), UserAdmin)
admin.site.register(WXUid, WeiBoAdmin)
