from os.path import join, os, exists

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem


def get_parent_items():
    menu = []
    apps_dir = join(settings.PROJECT_PATH, 'apps')
    for dirname in next(os.walk(apps_dir))[1]:
        if dirname not in ['accounts'] and exists(join(apps_dir, '{}/admin.py'.format(dirname))):
            menu.append(ParentItem(_('{}'.format(dirname)), app='{}'.format(dirname), icon='fa fa-heart'))
    return menu


class SuitConfig(DjangoSuitConfig):
    layout = 'vertical'
    menu = [
        ParentItem(_('accounts'), children=[
            ChildItem(model='accounts.user'),
            ChildItem(model='auth.group'),
            ChildItem(model='accounts.WBUid'),
        ], icon='fa fa-user'),
#         ParentItem(_('organizations'), app='organizations', icon='fa fa-signal'),
#         ParentItem(_('流程'), app='vetting', icon='fa fa-signal'),
#         ParentItem(_('附件'), app='annex', icon='fa fa-signal'),
#         ParentItem(_('票据'), app='bills', icon='fa fa-signal'),
#         ParentItem(_('files'), app='files', icon='fa fa-file'),
#         ParentItem(_('客户信息'), app='customers', icon='fa fa-file'),
#         ParentItem(_('联系人'), app='contacts', icon='fa fa-file'),
#         ParentItem(_('合同'), app='contracts', icon='fa fa-file'),
#         ParentItem(_('申请单'), app='orders', icon='fa fa-file'),
#         ParentItem(_('账户'), app='payment_accounts', icon='fa fa-file'),
        ParentItem(_('Documentation'), url='/developer/', icon='fa fa-book', target_blank=True),
        ParentItem(_('API'), url='/api/v1/', icon='fa fa-wrench', target_blank=True),
    ]
    menu += get_parent_items()

    def ready(self):
        super(DjangoSuitConfig, self).ready()
