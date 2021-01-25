import os
from os.path import exists, join
from django.conf import settings
from django.urls import include, path
from django.conf.urls import include, url
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView
from django.conf.urls.static import static

#
# urlpatterns = [path('', include('railguns.urls'))]
# # Vendor
# urlpatterns += [path('s3direct/', include('s3direct.urls'))]
# # projects
# urlpatterns += [
#     path('', include(('{}.apps.home.urls'.format(settings.PROJECT_NAME), 'home'), namespace='v1')),
#     path('api/v1/', include(('{}.apps.api.urls'.format(settings.PROJECT_NAME), 'api'), namespace='v1')),
#     # # path('api/v1/agreement/', include('{}.apps.agreements.urls'.format(settings.PROJECT_NAME), namespace='v1')),
#     path('i18n/', include(('django.conf.urls.i18n', 'i18n'), 'i18n')),
#     # path(
#     #     'robots.txt',
#     #     cache_page(60 * 60)(
#     #         TemplateView.as_view(
#     #             template_name='robots_{}.txt'.format(settings.ENV.name.lower()), content_type='text/plain'
#     #         )
#     #     )
#     # )
# ]


# RailgunS:
urlpatterns = [
    url(r'', include('railguns.urls'))
]

# 第三方:
urlpatterns += [
    url(r'^s3direct/', include('s3direct.urls')),
    # url(r'^captcha/', include('captcha.urls'))
]


urlpatterns += [
    url(r'^MP_verify_vaTCZxpCJ0QAlmTW\.txt', TemplateView.as_view(template_name='MP_verify_vaTCZxpCJ0QAlmTW.txt', content_type='text/plain')),
]


# 项目:
urlpatterns += [
    # url('', include(('{}.apps.urls'.format(settings.PROJECT_NAME), 'apps'), namespace='apps-urls')),
    url(r'^api/v1/', include(('{}.apps.api.urls'.format(settings.PROJECT_NAME), 'v1'), namespace='v1')),
    url(r'^article/', include('{}.apps.articles.urls'.format(settings.PROJECT_NAME, 'article'))),
    url(r'^home/', include('{}.apps.home.urls'.format(settings.PROJECT_NAME, 'home'))),
    # *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    # *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
#
apps_dir = join(settings.PROJECT_PATH, 'apps')
for dirname in next(os.walk(apps_dir))[1]:
    if dirname not in ['__pycache__', 'api',] and exists(join(apps_dir, '{}/urls.py'.format(dirname))):
        urlpatterns += [url(r'^{}/'.format(dirname), include('{}.apps.{}.urls'.format(settings.PROJECT_NAME, dirname)))]
#
