# -*- coding: utf-8 -*-
import oss2

from django.conf import settings


def get_sign_url(filename):
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    auth = oss2.Auth(settings.CLOUD_SS_ID, settings.CLOUD_SS_SECRET)
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth, settings.CLOUD_SS_BASE_DOMAIN_NAME, settings.BUCKET_MEDIA)

    # 设置此签名URL在60秒内有效。
    return bucket.sign_url('GET', filename, 60)
