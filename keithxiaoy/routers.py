"""
根据django的文档
https://docs.djangoproject.com/en/dev/topics/db/multi-db/#exposing-multiple-databases-in-django-s-admin-interface
说admin不支持多数据库路由, 实际看起来支持的挺好的, 待研究.
另根据django的ticket
https://code.djangoproject.com/ticket/14121
根据id的路由还是要到查询里自己去做
"""
from builtins import isinstance

from django.db.models.fields import BigIntegerField
from railguns.django.db.middleware import request_cfg
from railguns.django.db.utils import db_slave, get_user_id, db_master


class PrimaryReplicaRouter(object):

    def db_for_read(self, model, **hints):
        """
        直接对model做isinstance取到的都是ModelBase
        不能直接get_field('id'), 比如Token的pk为key. 如果 无主键 或 非分库表主键64位 有潜在错误可能.
        """
        if model._meta.model_name in ['order', 'offer', 'enquiry', 'transaction']:
            return db_slave()
        elif isinstance(model._meta.get_field(model._meta.pk.name), BigIntegerField):
            if request_cfg.pk:
                return db_slave(get_user_id(int(request_cfg.pk)))
        return db_slave()

    def db_for_write(self, model, **hints):
        """
        分库的 创建 和 更新 操作在模型类save处理
        分库的 删除 操作在接口手动处理, admin未来再说.
        """
        return db_master()

    def allow_relation(self, obj1, obj2, **hints):
        db_list = ('db_master', 'db_slave')  # TODO: 应该不对.
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        return True
