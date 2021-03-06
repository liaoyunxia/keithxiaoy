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
    path('api/v1/', include('{}.apps.api.urls.v1_urls'.format(settings.PROJECT_NAME), namespace='v1')),
    path('api/v2/', include('{}.apps.api.urls.v2_urls'.format(settings.PROJECT_NAME), namespace='v2')),
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
