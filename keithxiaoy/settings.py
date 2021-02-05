from __future__ import absolute_import, unicode_literals
from datetime import timedelta

from corsheaders.defaults import default_headers
from django.contrib import messages
from railguns.django.utils.translation import dj_gettext
from django.utils.translation import gettext_lazy as _
from .constants import *

TEST_ENV = False
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_NAME = os.path.basename(BASE_DIR)

DOMAIN_NAME = 'keithxiaoy.com'
BASE_URL = 'http://keithxiaoy.{}'.format(DOMAIN_NAME)  # www.是为了微信
API_VERSION = 'api/v1'

if TEST_ENV:
    SECRET_KEY = 'x*n#6#*036=bf3qxw8)g^i*_&5!36kuq(s9fr5z6pgunml8#=_'
else:
    SECRET_KEY = 'nafr1l@c+(r5xcd@%j&4z)^=-3x$be58s!^x^fepf@mjt#e+eh'

# 亚马逊或阿里云.
CLOUD = 'aliyun'  # 可选: aws, aliyun
CLOUD_ACCESS_KEY_ID = '4i1dOdt86fCut0qQ'
CLOUD_SECRET_ACCESS_KEY = 'ptfjVg5gyH1nrD2lHJaXu0bM9J6Met'
CLOUD_SIGNATURE_FILE = 'go/{}_ubuntu.signature'.format(CLOUD)
# CLOUD_STORAGE_BASE_DOMAIN_NAME = 'oss-cn-hangzhou.aliyuncs.com'  # region是oss-cn-hangzhou
BUCKET_MEDIA = '/media/'
BUCKET_STATIC = '/static/'
BUCKET_CLOUD = '/cloud/'
ALLOWED_HOSTS = ['http://www.keithxiaoy.cn', 'www.keithxiaoy.cn', '106.75.237.156', '127.0.0.1', 'localhost', '0.0.0.0']

# ALLOWED_HOSTS = ['.{}'.format(DOMAIN_NAME), '.compute-1.amazonaws.com']  # ELB和Gunicorn直接配暂时没找到转发Domain的解决方案
# ALLOWED_HOSTS.append('120.27.142.121')
if TEST_ENV:
    WHITE_IPS = ['127.0.0.1', '218.1.115.186', '120.27.142.121']
else:
    WHITE_IPS = ['106.75.237.156', '10.23.75.23']
# ALLOWED_HOSTS.append(socket.gethostbyname(socket.gethostname()))
# Internal Ip White name
# CSRF_TRUSTED_ORIGINS = ['.cpcn.com.cn']


INSTALLED_APPS = [
    '{}.app.SuitConfig'.format(PROJECT_NAME),
    'ckeditor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 第三方:
    'railguns',
    'rest_framework',
    'haystack',
    'import_export',
    's3direct',
    'mdeditor',
]
for dirname in next(os.walk(os.path.join(PROJECT_PATH, 'apps')))[1]:
    if dirname not in ['__pycache__']:
        INSTALLED_APPS += ['{}.apps.{}.apps.Config'.format(PROJECT_NAME, dirname)]
# TEST_RUNNER = '{}.apps.api.unit_test.run_tests'.format(PROJECT_NAME)
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'railguns.django.db.middleware.MultiDBRouterMiddleware',
    # '{}.middleware.RequestUserMiddleware'.format(PROJECT_NAME)
]

ROOT_URLCONF = '{}.urls'.format(PROJECT_NAME)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_PATH, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ]
        }
    }
]
WSGI_APPLICATION = '{}.wsgi.application'.format(PROJECT_NAME)

SHARD_COUNT = 2  # TODO:生产环境创建好128个库之后，此处应做对应修改.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'keithxiaoy_default',
        'USER': 'ubuntu',
        'PASSWORD': 'Liaoliao@1234',   # Setting when installing MySQL
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# DATABASE_ROUTERS = ['keithxiaoy.database_router.MasterSlaveRouter']
#
DATABASE_ROUTERS = ['keithxiaoy.database_router.PrimaryReplicaRouter']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '28b35754e0fa4364.m.cnhzaliet1finance001.ocs.aliyuncs.com:11211',
        'PREFIX': '{}:'.format(PROJECT_NAME)
    }
}
REDIS = {
    'HOST': 'e6837b0ac94b4118.m.cnhza.kvstore.aliyuncs.com',
    'PORT': 6379,
    'DB': 0,
    'PASSWORD': 'e6837b0ac94b4118:ReO119fh1c'
}

KV_REDIS = 'develop-redis-app.develop.svc.cluster.local'
KV_REDIS_PASSWORD = 'Redis666666'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6
        }
    }
]

TIME_ZONE = 'Asia/Shanghai'
LANGUAGES = [
    ('en', _('English')),
    ('ja', _('Japanese')),
    ('zh-hans', _('Simplified Chinese'))
]
LOCALE_PATHS = [
    os.path.join(PROJECT_PATH, 'locale')
]
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(PROJECT_PATH, 'static'),
]

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = '/'

EMAIL_HOST = 'smtpdm.aliyun.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'test@notice.cmcaifu.com'
EMAIL_HOST_PASSWORD = '12345qwert'
DEFAULT_FROM_EMAIL = 'test@notice.cmcaifu.com'
EMAIL_SUBJECT_PREFIX = DOMAIN_NAME
# 💟 第三方:
# Django REST framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        #h5要关
        # 'rest_framework.authentication.SessionAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
        # 'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    'DEFAULT_PAGINATION_CLASS': 'railguns.rest_framework.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 150,  # TODO: 暂时100, 待做axois上拉加载更多
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter'
    ],
    'DATETIME_FORMAT': '%s',
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/second',
        'user': '10/second'
    }
}
# yapf: enable

# if ENV == STAGE.PRO:
REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = ['rest_framework.permissions.AllowAny']

# Dj

# Django REST framework JWT
JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'railguns.rest_framework_jwt.utils.jwt_response_payload_handler',
    'JWT_EXPIRATION_DELTA': timedelta(days=90),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=90)
}

# # Django REST Swagger
# SWAGGER_SETTINGS = {
#     'exclude_namespaces': ['v1'],
#     'api_version': 'v2.0.0',
#     'api_path': '/',  # Specify the path to your API not a root level
#     'api_key': '',  # An API key
#     'is_authenticated': True,
#     'is_superuser': True,
#     'info': {
#         'title': '{} API 文档'.format(DOMAIN_NAME),
#         'description': 'v2.0.0'
#     },
#     'doc_expansion': 'list'
#     #     'SECURITY_DEFINITIONS': {
#     #         'basic': {
#     #             'type': 'basic'
#     #         }
#     #     },
#     #     'APIS_SORTER': 'alpha',
#     #     'DOC_EXPANSION': 'list'
# }

# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'MUST',
        'INDEX_NAME': 'haystack'
    }
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'


# django-s3direct
def create_filename(filename):
    import uuid
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4().hex, ext)
    return os.path.join('uploads/images', filename)


S3DIRECT_DESTINATIONS = {
    'imgs': ('uploads/photoplus', lambda u: u.is_staff(), True, ['image/jpeg', 'image/png'],),
    'vids': ('uploads/vids', lambda u: u.is_staff(), ['video/mp4'],),
    # Allow logged in users to upload any type of file and give it a private acl:
    'custom_filename': (create_filename,),
    'private': (
        'uploads/vids',
        lambda u: u.is_authenticated(),
        '*',
        'private')
}

# Django Modeltranslation
MODELTRANSLATION_DEFAULT_LANGUAGE = 'zh-hans'
MODELTRANSLATION_FALLBACK_LANGUAGES = {
    'default': ('zh-hans', 'en'),
    'ja': ('ja', 'en')
}


# Django CKEditor
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'width': 700,
        'height': 500,
        'removePlugins': 'stylesheetparser',
    }
}


# Django Simple Captcha
CAPTCHA_FONT_SIZE = 40
CAPTCHA_FOREGROUND_COLOR = 'red'

# """💟 以下为测试环境配置"""
# if TEST_ENV:
#     DEBUG = False  # 测试环境Debug默认关闭, 以免测试环境正常而生产环境却出现500错误
#     HTML_MINIFY = True  # 测试环境不最小化html
#     BASE_URL = 'http://factor.{}'.format(DOMAIN_NAME)
#     BUCKET_MEDIA = 'test-{}'.format(BUCKET_MEDIA)
#     BUCKET_STATIC = 'test-{}'.format(BUCKET_STATIC)
#     BUCKET_CLOUD = 'test-{}'.format(BUCKET_CLOUD)
#     SHARD_COUNT = 0
#     DATABASES['default']['HOST'] = 'testcmcaifu.mysql.rds.aliyuncs.com'
#     CACHES['default']['LOCATION'] = '127.0.0.1:11211'
#     REDIS['HOST'] = '10.117.182.179'
#     REDIS['PASSWORD'] = None
    # 以下在 前端工程师 需要时开启:
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE += ['corsheaders.middleware.CorsMiddleware']
CORS_ORIGIN_ALLOW_ALL = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {  #
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}
    },
    'filters': {  #
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {  #
        'debug': {  #
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, "log", 'django.log'),  #
            'formatter': 'standard',  # formatters
        },
        'error': {  #
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, "log", 'error.log'),  #
            'formatter': 'standard',  #
        },
        'facebook': {  #
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, "log", 'facebook.log'),
            'formatter': 'standard',
        },
        'task': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, "log", 'task.log'),
            'formatter': 'standard',
        },
        'third': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, "log", 'third.log'),
            'formatter': 'standard',
        },
        'pay': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, "log", 'pay.log'),
            'formatter': 'standard',
        },
        'rpc': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, "log", 'rpc.log'),
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'include_html': True,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['debug', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['debug', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'error': {
            'handlers': ['error', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
        'facebook': {
            'handlers': ['facebook', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
        'task': {
            'handlers': ['task', 'mail_admins'],
            'level': 'INFO',
            'propagate': True
        },
        'third': {
            'handlers': ['third', 'mail_admins'],
            'level': 'INFO',
            'propagate': True
        },
        'pay': {
            'handlers': ['pay', 'mail_admins'],
            'level': 'INFO',
            'propagate': True
        },
        'rpc': {
            'handlers': ['rpc', 'mail_admins'],
            'level': 'INFO',
            'propagate': True
        },
    }
}