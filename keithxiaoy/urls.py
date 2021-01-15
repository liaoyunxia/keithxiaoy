import os
from os.path import exists, join

from django.conf import settings
from django.conf.urls import include, url
from django.views.generic.base import TemplateView


from django.conf import settings
from django.urls import include, path
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView

# Railgun S
urlpatterns = [path('', include('railguns.urls'))]
# Vendor
urlpatterns += [path('s3direct/', include('s3direct.urls'))]
# projects
urlpatterns += [
    path('', include('{}.apps.website.urls'.format(settings.PROJECT_NAME), namespace='website')),
    path('api/v1/', include('{}.apps.api.urls'.format(settings.PROJECT_NAME), namespace='v1')),
    # path('api/v1/agreement/', include('{}.apps.agreements.urls'.format(settings.PROJECT_NAME), namespace='v1')),
    path('i18n/', include('django.conf.urls.i18n')),
    path(
        'robots.txt',
        cache_page(60 * 60)(
            TemplateView.as_view(
                template_name='robots_{}.txt'.format(settings.ENV.name.lower()), content_type='text/plain'
            )
        )
    )
]

#
# urlpatterns += [
#     url(r'^MP_verify_vaTCZxpCJ0QAlmTW\.txt', TemplateView.as_view(template_name='MP_verify_vaTCZxpCJ0QAlmTW.txt', content_type='text/plain')),
# ]
#
#
# # 项目:
# urlpatterns += [
#     path('api/v1/', include('{}.apps.api.urls.v1_urls'.format(settings.PROJECT_NAME), namespace='v1')),
#     url(r'^api/v1/', include('{}.apps.api.urls'.format(settings.PROJECT_NAME), 'v1'), namespace='v1'),
#     url(r'', include('{}.apps.home.urls'.format(settings.PROJECT_NAME))),
# ]
#
# apps_dir = join(settings.PROJECT_PATH, 'apps')
for dirname in next(os.walk(apps_dir))[1]:
    if dirname not in ['__pycache__', 'api', 'home'] and exists(join(apps_dir, '{}/urls.py'.format(dirname))):
        urlpatterns += [path(r'^{}/'.format(dirname), include('{}.apps.{}.urls'.format(settings.PROJECT_NAME, dirname)))]

