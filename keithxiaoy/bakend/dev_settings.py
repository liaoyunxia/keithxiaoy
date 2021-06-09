from django.test.runner import DiscoverRunner

from .settings import *

DEBUG = True
MESSAGE_LEVEL = messages.DEBUG
ENV = STAGE.DEV

# MEDIA_URL = 'https://{}.{}/'.format(BUCKET_MEDIA, CLOUD_SS_BASE_DOMAIN_NAME)

SECURE_PROXY_SSL_HEADER = None
SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

SECRET_KEY = '_)b$x8t_*!-$@(kpn4y#^h-tp$8t&*bn-j14d0yz_0_hj3%wvf'
BASE_URL = 'http://localhost:5000'  # FIXME: will case error when run 8001
ALLOWED_HOSTS = [
    # DJ: https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
    'localhost',
    '127.0.0.1',
    '[::1]',
    '10.1.7.25',
    '10.1.3.224',
    '*',
]
INTERNAL_IPS = [
    '127.0.0.1',
    '10.1.7.25',
    '10.1.3.224',
]  # append and after open debug AND debug_toolbar, ONLY 127.0.0.1 NOT localhost
WHITELIST = [
    '127.0.0.1',
    '10.1.7.25',
    '10.1.3.224',
]

SHARD_COUNT = 0

DB_NAME = 'jk_p2p_app_dev'
DB_USER = 'dev'
DB_PASS = '360Kredi'
RDS = '10.51.28.89'
RDS_READ = '10.51.28.89'

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
    'read': {
        'NAME': DB_NAME,
        'HOST': RDS_READ,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'ENGINE': 'django.db.backends.mysql',
        # 'CONN_MAX_AGE': 120,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'sql_mode': 'TRADITIONAL'
        },
    }
}
for i in range(SHARD_COUNT):
    # noinspection PyUnresolvedReferences
    db_dict = DATABASES['default'].copy()
    db_dict['NAME'] = '{}_{}'.format(PROJECT_NAME, i)
    DATABASES['db_{}'.format(i)] = db_dict

KV_REDIS = '127.0.0.1'
KV_REDIS_PASSWORD = None

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://{}:6379/1'.format(KV_REDIS),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

# Celery settings
CELERY_BROKER_URL = 'redis://:{}@{}:6379/2'.format(KV_REDIS_PASSWORD, KV_REDIS),

# Django REST framework
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += [
    'rest_framework.renderers.BrowsableAPIRenderer', 'rest_framework.renderers.AdminRenderer'
]
REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = []  #

# Haystack
HAYSTACK_CONNECTIONS['default']['URL'] = 'http://127.0.0.1:9200/'
# HAYSTACK_MOD = 4
# for i in range(HAYSTACK_MOD):
#     haystack_dict = HAYSTACK_MOD['default'].copy()
#     haystack_dict['name'] = '{}_{}'.format(PROJECT_NAME, i)
#     HAYSTACK_CONNECTIONS['hay_{}'.format(i)] = haystack_dict

REVIEW_SYSTEM_HOST = 'http://test.data.dokuin.id'
REVIEW_SYSTEM_ID = 'hyLNxaOGIWlkHl2AtcByUdUF4BbnyPWfRdNdxSEG'
REVIEW_SYSTEM_SECRET = '3CQW0vIzWhQbg7WxmYbbmwYpwfsUvyOijUr1zth1XveOugQ4hS2aGGSIvXseE3EVUl2Op4GBxrlr9r9o9jf5cMxz4XmoEU6Au2iCLKUopvbDlkgRTeTK2offBb3ZNsDx'

# Aliyun RocketMQ
ROCKET_MQ_HTTP_ENDPOINT = 'http://MQ_INST_5426565869997950_BcUgG0k8.ap-southeast-5.mq-internal.aliyuncs.com:8080'
ROCKET_MQ_ACCESS_KEY = 'LTAI4GCByM7Ryd9Gvvay9Xfx'
ROCKET_MQ_SECRET_KEY = 'iovn6Jv96YXRr8HyWthqC1xAt0YpFu'
ROCKET_MQ_INSTANCE_ID = 'MQ_INST_5426565869997950_BcUgG0k8'

# mop Aliyun RocketMQ
MOP_ROCKET_MQ_ACCESS_KEY = 'LTAI4G6dLxJUoSqc4CbcD2ba'
MOP_ROCKET_MQ_SECRET_KEY = 'KVW2slrhSOy2YHB9HHu1LpNeEzSnOp'
MOP_ROCKET_MQ_TCP_GROUP_ID = 'GID_MOP_1'
MOP_ROCKET_MQ_HTTP_GROUP_ID = 'GID_MOP_2'
MOP_ROCKET_MQ_TOPIC_NAME = 'mop-tag-topic'
MOP_ROCKET_MQ_INSTANCE_ID = 'MQ_INST_5289168616669439_BXgMFpS9'
MOP_ROCKET_MQ_TCP_ENDPOINT = 'http://{}.ap-southeast-5.mq-internal.aliyuncs.com:8080'.format(MOP_ROCKET_MQ_INSTANCE_ID)
MOP_ROCKET_MQ_HTTP_ENDPOINT = 'http://5289168616669439.mqrest.ap-southeast-5.aliyuncs.com'
MOP_ROCKET_MQ_HTTP_INTERNAL_ENDPOINT = 'http://5289168616669439.mqrest.ap-southeast-5-internal.aliyuncs.com'

# Config to be passed to ClusterRpcProxy
NAMEKO_CONFIG = {
    'AMQP_URI': 'amqp://127.0.0.1:5672/',
}

# Set timeout for RPC
NAMEKO_TIMEOUT = 5  # timeout

# Stop part of the business
BUSINESS_STOP_PARTIAL = False

# django-htmlmin
HTML_MINIFY = False

# Django Rosetta
ROSETTA_MESSAGES_PER_PAGE = 20

# Django silk settings
SILKY_PYTHON_PROFILER = True
SILKY_PYTHON_PROFILER_BINARY = True

TEST_RUNNER = 'jk_p2p_app.dev_settings.NoDbTestRunner'


# testing utils and settings
class NoDbTestRunner(DiscoverRunner):
    """ A test runner to test without database creation """
    def setup_databases(self, **kwargs):
        """ Override the database creation defined in parent class """
        pass

    def teardown_databases(self, old_config, **kwargs):
        """ Override the database teardown defined in parent class """
        pass


GRPC_HOST = 'kong.develop.svc.cluster.local'
