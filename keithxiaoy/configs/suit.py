from django.utils.translation import ugettext_lazy as _


CONFIG = {
    'SEARCH_URL': '/admin/accounts/user/',
    'MENU': [
        'sites',
        {'label': _('accounts'), 'icon': 'icon-user',
         'models': ('accounts.user',
                    'auth.group',
                    {'label': 'weibo', 'model': 'accounts.WBUid'},
                    )},
        {'app': 'organizations', 'label': _('organizations'), 'icon': 'icon-signal'},
        {'app': 'vetting', 'label': _('流程'), 'icon': 'icon-signal'},
        '-',
        {'app': 'files', 'label': _('files'), 'icon': 'icon-file'},
        {'app': 'customers', 'label': _('客户信息'), 'icon': 'icon-signal'},
        {'app': 'contacts', 'label': _('联系人'), 'icon': 'icon-signal'},
        {'app': 'contracts', 'label': _('合同'), 'icon': 'icon-signal'},
        '-',
        {'app': 'orders', 'label': _('申请单'), 'icon': 'icon-signal'},
        {'app': 'payment_accounts', 'label': _('账户'), 'icon': 'icon-signal'},
        {'app': 'annex', 'label': _('附件'), 'icon': 'icon-signal'},
        '-',
        {'label': 'Documentation', 'icon': 'icon-book', 'url': '/developer/', 'blank': True},
        {'label': 'API', 'icon': 'icon-wrench', 'url': '/api/v2/', 'blank': True},
        {'label': 'AWS', 'icon': 'icon-hdd', 'url': 'http://console.amazonaws.cn', 'blank': True},
        {'label': 'DNS', 'icon': 'icon-hdd', 'url': 'http://netcn.console.aliyun.com/core/domain/list', 'blank': True},
        '-',
        {'label': 'Redis', 'icon': 'icon-tasks', 'url': '/admin/redisboard/redisserver/'}
    ]
}
