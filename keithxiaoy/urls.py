import os
from os.path import exists, join

from django.conf import settings
from django.conf.urls import include, url
from django.views.generic.base import TemplateView


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
    url(r'^api/v1/', include('{}.apps.api.urls'.format(settings.PROJECT_NAME), namespace='v1')),
    url(r'', include('{}.apps.home.urls'.format(settings.PROJECT_NAME))),
]

apps_dir = join(settings.PROJECT_PATH, 'apps')
for dirname in next(os.walk(apps_dir))[1]:
    if dirname not in ['__pycache__', 'api', 'home'] and exists(join(apps_dir, '{}/urls.py'.format(dirname))):
        urlpatterns += [url(r'^{}/'.format(dirname), include('{}.apps.{}.urls'.format(settings.PROJECT_NAME, dirname)))]
