from __future__ import absolute_import, unicode_literals
from datetime import timedelta

from corsheaders.defaults import default_headers
from django.contrib import messages
from railguns.django.utils.translation import dj_gettext

from keithxiaoy.constants import *

# Celery settings
CELERY_BROKER_URL = 'redis://:{}@{}:6379/2'.format(KV_REDIS_PASSWORD, KV_REDIS),
CELERY_ACCEPT_CONTENT = ['json']
# CELERY_RESULT_BACKEND = 'redis://{}:6379/2'.format(KV_REDIS),
CELERY_TASK_SERIALIZER = 'json'
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'Asia/Jakarta'

CELERYD_CONCURRENCY = 8
CELERYD_FORCE_EXECV = True
CELERYD_MAX_TASKS_PER_CHILD = 100
CELERY_DISABLE_RATE_LIMITS = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_NAME = os.path.basename(BASE_DIR)

SECURE_PROXY_SSL_HEADER = SSL_HEADER
SESSION_COOKIE_DOMAIN = DOMAIN_NAME
SESSION_COOKIE_SECURE = COOKIE_SECURE
CSRF_COOKIE_SECURE = CSRF_SECURE
# CSRF_TRUSTED_ORIGINS = ['.cpcn.com.cn']

DEBUG = False

ALLOWED_HOSTS = [SESSION_COOKIE_DOMAIN]  # ELB AND Gunicorn DERECT SETTING, COULD'T FIND THE WAY TO Domain
ALLOWED_HOSTS += SLB
ALLOWED_HOSTS += OTHER_DOMAIN
if DEBUG:
    ALLOWED_HOSTS += ECS
    MESSAGE_LEVEL = messages.DEBUG

INSTALLED_APPS = [
    '{}.app.SuitConfig'.format(PROJECT_NAME),
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Railgun S
    'railguns',
    'rest_framework',
    'ckeditor',
    'crispy_forms',
    'django_extensions',
    'django_filters',
    'drf_yasg',
    # Vendor
    'haystack',
    'import_export',
]
for dirname in next(os.walk(os.path.join(PROJECT_PATH, '../apps')))[1]:
    if dirname not in ['__pycache__']:
        INSTALLED_APPS += ['{}.apps.{}.apps.Config'.format(PROJECT_NAME, dirname)]
# TEST_RUNNER = '{}.apps.api.unit_test.run_tests'.format(PROJECT_NAME)
if ENV == STAGE.PROD:
    SECRET_KEY = '+@b5e1nb)fng6^7pa+wkosk1ymhv=m3w)wqrtcj2rcv5d=tg8f'
    INSTALLED_APPS += ['corsheaders']
    MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware']
    # CORS_ORIGIN_ALLOW_ALL = True
else:
    SECRET_KEY = 'wyam5*srsb%$ixst$vzz!32^dp07!%j9sfsd)s+rpnhl-(syt+'
    INSTALLED_APPS += ['corsheaders']
    MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware']
    CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    'channel',
    'version-name'
]

MIDDLEWARE += [
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
    'django.middleware.common.BrokenLinkEmailsMiddleware',

    # custom middleware
    'jk_p2p_app.apps.accounts.middleware.CloseUserMiddleware',
    'jk_p2p_app.apps.accounts.middleware.GenericMiddleware',

    # django_currentuser, htmlmin
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
]

ROOT_URLCONF = '{}.urls'.format(PROJECT_NAME)

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(PROJECT_PATH, '../templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ]
    }
}]  # yapf: disable
WSGI_APPLICATION = '{}.wsgi.application'.format(PROJECT_NAME)

SHARD_COUNT = 0  # TODO:
DATABASES = {
    'default': {
        'NAME': DB_NAME,
        'HOST': RDS,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'ENGINE': 'django.db.backends.mysql',
        # 'CONN_MAX_AGE': 120,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'sql_mode': 'TRADITIONAL'
        },
    },
    # 'read': {
    #     'NAME': DB_NAME,
    #     'HOST': RDS_READ,
    #     'USER': DB_USER,
    #     'PASSWORD': DB_PASS,
    #     'ENGINE': 'django.db.backends.mysql',
    #     'OPTIONS': {
    #         'charset': 'utf8mb4',
    #         'sql_mode': 'TRADITIONAL'
    #     },
    # }
}

DATABASE_ROUTERS = ['jk_p2p_app.database_router.MasterSlaveRouter']

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://{}:6379/1'.format(KV_REDIS),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'COMPRESSOR': 'django_redis.compressors.lzma.LzmaCompressor',
            'IGNORE_EXCEPTIONS': True,
            'PASSWORD': KV_REDIS_PASSWORD
        }
    }
}

PASSWORD_HASHERS = ['django.contrib.auth.hashers.Argon2PasswordHasher']

AUTH_PASSWORD_VALIDATORS = [{
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
}, {
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    'OPTIONS': {
        'min_length': 6
    }
}]

TIME_ZONE = 'Asia/Jakarta'
LANGUAGES = [('id', dj_gettext('Indonesia')), ('en', dj_gettext('English'))]
LANGUAGE_CODE = 'id'
LOCALE_PATHS = [os.path.join(PROJECT_PATH, '../locale')]
USE_L10N = True
USE_TZ = True

# MEDIA_URL = '/media/'
# STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

ACCESS_KEY_ID = CLOUD_SS_ID
ACCESS_KEY_SECRET = CLOUD_SS_SECRET
END_POINT = CLOUD_SS_BASE_DOMAIN_NAME
BUCKET_NAME = BUCKET_MEDIA
ALIYUN_OSS_CNAME = ""  # custom domain
BUCKET_ACL_TYPE = "public-read"  # private, public-read, public-read-write

DEFAULT_FILE_STORAGE = 'aliyun_oss2_storage.backends.AliyunMediaStorage'
# STATICFILES_STORAGE = 'aliyun_oss2_storage.backends.AliyunStaticStorage'

MEDIA_URL = 'https://{}.{}/'.format(BUCKET_MEDIA, CLOUD_SS_BASE_DOMAIN_NAME)
STATIC_URL = 'https://{}.{}/'.format(BUCKET_STATIC, CLOUD_SS_BASE_DOMAIN_NAME)
STATICFILES_DIRS = [os.path.join(PROJECT_PATH, '../static')]

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

if ENV == STAGE.PROD:
    ADMINS = [
        ('yinjiaqing', 'josephyin@outlook.com'),
        ('laioyunxia', '372021030@qq.com'),
        ('xujiale', 'xjl59667135@outlook.com'),
        ('yubo', 'josh.yu_8@live.com'),
    ]
else:
    ADMINS = [
        ('yubo', 'josh.yu_8@live.com'),
        ('laioyunxia', '372021030@qq.com'),
    ]
MANAGERS = ADMINS
SEND_BROKEN_LINK_EMAILS = True
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = f'[{DOMAIN_NAME}] '
DEFAULT_FROM_EMAIL = 'admin@notice.{}'.format(DOMAIN_NAME)
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'josephyjq@gmail.com'
EMAIL_HOST_PASSWORD = 'vjwmmnnwhpnrvuqm'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/admin/login/'  # can't use  /admin/login/, will link normal user can't login
LOGIN_REDIRECT_URL = '/task/'
LOGOUT_URL = '/admin/logout/'

# 💟 Vendor
# Django REST framework
# yapf: disable
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_VERSION': 'v2',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    'DEFAULT_PAGINATION_CLASS': 'railguns.rest_framework.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 150,  #
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter'
    ],
    'DATETIME_FORMAT': '%s',
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/second',
        'user': '10/second',
        'sendpush': '1000/second',
        'sendsms': '1000/second',
    }

}
# yapf: enable

# Django REST framework JWT
JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': '{}.apps.utils.jwt_response_payload_handler'.format(PROJECT_NAME),
    'JWT_EXPIRATION_DELTA': timedelta(days=30),
    # 'JWT_EXPIRATION_DELTA': timedelta(minutes=1),
    # 'JWT_EXPIRATION_DELTA': timedelta(seconds=15),
    # 'JWT_EXPIRATION_DELTA': timedelta(hours=1),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=30)
}

# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'MUST',
        'INDEX_NAME': 'haystack'
    }
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Django CKEditor
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'width': 700,
        'height': 500,
        'removePlugins': 'stylesheetparser'  #
    }
}

# db counts
for i in range(SHARD_COUNT):
    db_dict = DATABASES['default'].copy()
    db_dict['NAME'] = '{}_{}'.format(PROJECT_NAME, i)
    DATABASES['db_{}'.format(i)] = db_dict

# logging settings
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
