# https://github.com/darklow/django-suit/blob/v2/suit/apps.py

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from railguns.django.utils.translation import dj_gettext
from suit.apps import DjangoSuitConfig
from suit.menu import ChildItem, ParentItem


class SuitConfig(DjangoSuitConfig):
    app_name = _('app_name')
    verification_code = _('verification_code')
    menu_show_home = False

    # JUST FOR TRANSLATE
    # https://fontawesome.com/v4.7.0/icons/ ICONS
    layout = 'vertical'
    menu = []
    # if settings.ENV == settings.STAGE.DEV:
        # menu += [ParentItem(_('architect'), app='architect', icon='fa fa-fw fa-building')]
    menu += [
        ParentItem(_('accounts'), app='accounts', icon='fa fa-fw fa-user'),
        ParentItem(_('analysis'), app='analysis', icon='fa fa-fw fa-book'),
        ParentItem(_('products'), app='products', icon='fa fa-fw fa-shopping-bag'),
        ParentItem(_('agreements'), app='agreements', icon='fa fa-fw fa-book'),
        ParentItem(_('orders'), app='orders', icon='fa fa-fw fa-shopping-cart'),
        ParentItem(_('transactions'), app='transactions', icon='fa fa-fw fa-exchange'),
        ParentItem(_('reviews'), app='review', icon='fa fa-fw fa-tasks'),
        ParentItem(_('content'), app='content', icon='fa fa-fw fa-bookmark'),
        ParentItem(_('files'), app='files', icon='fa fa-fw fa-files-o'),
        ParentItem(_('credit'), app='credit', icon='fa fa-fw fa-star'),
        ParentItem(_('thirddata'), app='thirddata', icon='fa fa-fw fa-files'),
        ParentItem(_('featured'), app='featured', icon='fa fa-fw fa-star'),
        ParentItem(_('notifications'), app='notification', icon='fa fa-fw fa-bell'),
        # ParentItem(_('site'), app='site', icon='fa fa-fw fa-heart'),
        ParentItem(_('marketing'), app='marketing', icon='fa fa-fw fa-heart'),
        ParentItem(_('logs'), children=[ChildItem(model='logs.systemoperationlog'),
                                        ChildItem(model='admin.logentry')], icon='fa fa-fw fa-bookmark'),
        ParentItem(_('settings'), children=[ChildItem(model='auth.group')], icon='fa fa-fw fa-cog')
    ]
    # MORE LANGUAGE
    if settings.ENV == settings.STAGE.DEV:
        menu += [
            ParentItem(
                'rosetta',
                url='/rosetta/files/project/zh-hans/0/?ref_lang=msgid&msg_filter=untranslated',
                icon='fa fa-fw fa-globe',
                target_blank=True),
        ]
