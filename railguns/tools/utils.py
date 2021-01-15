import locale

from django.conf import settings


def locale_currency(currency, amount):
    if settings.ENV == settings.STAGE.DEV:
        locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
    else:
        if currency == 'CNY':
            locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
        elif currency == 'IDR':
            locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
        else:
            locale.setlocale(locale.LC_ALL, '')

    locale._override_localeconv = {'n_sign_posn': 1}
    locale._override_localeconv = {'frac_digits': 0}
    return locale.currency(amount, grouping=True)
