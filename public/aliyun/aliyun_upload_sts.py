#!/usr/bin/env python
# coding=utf-8
import json
from urllib.parse import quote, urlencode

from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider
from aliyunsdksts.request.v20150401 import AssumeRoleRequest

import oss2
from django.conf import settings

REGIONID = 'ap-southeast-5'
ENDPOINT = 'sts.ap-southeast-5.aliyuncs.com'

def fetch_sts_token(username):
    # 配置要访问的STS Endpoint
    region_provider.add_endpoint('Sts', REGIONID, ENDPOINT)
    # 初始化Client
    clt = client.AcsClient(settings.STS_AK, settings.STS_SK, REGIONID)
    # 构造"AssumeRole"请求
    request = AssumeRoleRequest.AssumeRoleRequest()
    # 指定角色
    request.set_RoleArn(settings.STS_ROLE_ARN)
    # 设置会话名称，审计服务使用此名称区分调用者
    request.set_RoleSessionName('kartu-uang-{}'.format(username))
    # 发起请求，并得到response
    response = clt.do_action_with_exception(request)
    j = json.loads(oss2.to_unicode(response))
    return j['Credentials']


import time
import datetime
import json
import base64
import hmac
from hashlib import sha1 as sha
import collections
import operator
import uuid
import requests


def get_oss_signature(params, sk, http_method):
    assert http_method in ["GET", "POST", "PUT"]
    assert isinstance(params, dict)
    policy_dict = collections.OrderedDict(sorted(params.items(), key=operator.itemgetter(0)))
    policy_encode = '{}&%2F&{}'.format(http_method, quote(urlencode(policy_dict)))
    policy_encode = policy_encode.encode('utf-8')
    new_sk = '{}&'.format(sk)
    new_sk = new_sk.encode('utf-8')
    h = hmac.new(new_sk, policy_encode, sha)
    sign_result = base64.encodestring(h.digest()).strip()
    return sign_result


def get_oss_sts_token(username):
    param = {'AccessKeyId': settings.STS_AK,
             'Action': 'AssumeRole',
             'Format': 'JSON',
             'RoleArn': settings.STS_ROLE_ARN,
             'RoleSessionName': 'kartu-uang-{}'.format(username),
             'SignatureMethod': 'HMAC-SHA1',
             'SignatureNonce': str(uuid.uuid4()),
             'SignatureVersion': '1.0',
             'Timestamp': datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%SZ'),
             'Version': '2015-04-01'}
    url = 'https://sts.aliyuncs.com'

    param['Signature'] = get_oss_signature(param, settings.STS_SK, "GET")
    res = requests.get(url=url, params=param, timeout=60)

    if res.status_code / 100 != 2:
        return ''
    res_data = res.json()
    if 'Credentials' not in res_data:
        return ''
    return res_data['Credentials']
