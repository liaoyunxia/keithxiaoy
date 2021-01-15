# -*- coding: utf-8 -*-
import os
from enum import Enum

# 所有变量必须大写，否则无法通过django.conf.settings引入
# DJ: https://docs.djangoproject.com/en/dev/topics/settings/#creating-your-own-settings
STAGE = Enum('Stage', ['DEV', 'TEST', 'STAGING', 'PROD',])

ENV = STAGE.PROD

# according 12-factor, using environment
ENV = STAGE[os.environ.get('ENV')] if os.environ.get('ENV') else ENV

DOMAIN_NAME = 'www.keithxiaoy.cn'
BASE_URL = 'http://{}'.format(DOMAIN_NAME)  # 标准配置不要改动 (www.是为了微信)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_NAME = os.path.basename(BASE_DIR)

# 云计算服务
CLOUD = 'aliyun'  # 可选: aliyun, aws
# CLOUD_COMPANY_ALIAS = 'pintu_uang'  # 阿里云 管理控制台 -> 访问控制 -> 设置

# CLOUD_SMS_ID = ''
# CLOUD_SMS_SECRET = '6320970211ff1dcb9748a4a4343203c6'
# CLOUD_SMS_SIGN_NAME = 'Peanut'
# CLOUD_IDENTITY_SECRET = '60e42b03c68f1bb0a4db54a905d81f7d'
#
# STS_AK = 'LTAI4Fm9mZM14K2kz2uvr4es'
# STS_SK = 'yzASuMjVEAmp4M1FDQqHyFp2vjN8RP'
# STS_ROLE_ARN = 'acs:ram::5426565869997950:role/aliyunosstokengeneratorrole'

# CLOUD_SS_ID = 'LTAI4FmwjXKXKJgWKebM82qY'
# CLOUD_SS_SECRET = 'eyAmlHBqqYGt8YTVypDDHQ3fWJsfLm'

# CLOUD_SS_BASE_DOMAIN_NAME = 'oss-ap-southeast-5.aliyuncs.com'  # region是oss-区域
# CLOUD_SS_BASE_DOMAIN_NAME = "oss-accelerate.aliyuncs.com"
BUCKET_MEDIA = '/media'.format('')
BUCKET_STATIC = '/static-{}'.format('')
BUCKET_CLOUD = 'cloud-{}'.format('360-kredi-id')

MEDIA_URL = '/media/'.format(BUCKET_MEDIA)
STATIC_URL = '/static/'.format(BUCKET_STATIC)
STATICFILES_DIRS = (
    os.path.join(os.path.join(BASE_DIR, 'static')),
)

CORS_ORIGIN_WHITELIST = ('http://keithxiaoy.cn', )
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# 服务器
SLB = [
]  #
ECS = [
    '',
]  # OUTER IP

OTHER_DOMAIN = ['106.75.237.156',]

RDS = 'rm-.mysql.ap-southeast-5.rds.aliyuncs.com'
RDS_READ = 'rm-.mysql.ap-southeast-5.rds.aliyuncs.com'


DB_NAME = 'keithxiaoy_default'
DB_USER = 'root'
DB_PASS = 'Liao0726'
WHITELIST = [
    '10.23.75.23',
]

SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')
COOKIE_SECURE = True
CSRF_SECURE = True
# SSL_HEADER = None
# COOKIE_SECURE = False
# CSRF_SECURE = False
# Config to be passed to ClusterRpcProxy

# 样式
THEME = 'weui'

if ENV == STAGE.DEV:
    pass