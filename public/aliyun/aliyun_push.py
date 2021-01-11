# coding:utf-8

from base64 import b64encode
import datetime
import hashlib
import hmac
import random
from urllib.parse import quote

import requests


now = datetime.datetime.isoformat(datetime.datetime.utcnow()).split('.')[0] + 'Z'


class ALiYunPush():
    def __init__(self):
        self.AppSecrt = 'RTwvDfFNmMGro4C3f5vaBUMwggs6dx'    # Access key secret
        self.AppKey = '23388803'                            # TV安卓的appKey
        self.AccessKeyId = 'SdXIxSdYn0JtVaQv'
        self.Version = '2015-08-27'

    def now(self):
        return datetime.datetime.isoformat(datetime.datetime.utcnow()).split('.')[0] + 'Z'

    def createNoncestr(self, length=32):
        """产生随机字符串，不长于32位"""
        chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
        strs = []
        for x in range(length):
            strs.append(chars[random.randrange(0, len(chars))])
        return "".join(strs)

    def set_parameters(self, devices):
        parameters = {}
        parameters['RegionId'] = 'cn-hangzhou'
        parameters['Version'] = self.Version
        parameters['AccessKeyId'] = self.AccessKeyId
        parameters['SignatureMethod'] = 'HMAC-SHA1'
        parameters['Timestamp'] = '{}'.format(self.now())
        parameters['SignatureVersion'] = '1.0'
        parameters['SignatureNonce'] = self.createNoncestr(32)

        parameters['Action'] = 'Push'
        parameters['AppKey'] = self.AppKey

        parameters['Remind'] = 'true'              # 仅用于IOS通知，仅用于生产环境
        parameters['StoreOffline'] = 'false'              # 离线不保存.
        parameters['Type'] = '0'                         # 0表示消息1表示通知

        parameters['DeviceType'] = '1'  # 必须选择某一类型，若选3全选则推送不到
        parameters['Target'] = 'device'
        parameters['TargetValue'] = devices
        return parameters

    def formatBizQueryParaMap(self, paraMap, urlencode):
        """格式化参数，签名过程需要使用"""
        slist = sorted(paraMap)
        buff = []
        for k in slist:
            v = quote(paraMap[k]) if urlencode else paraMap[k]
            buff.append("{0}={1}".format(k, v))
        return "&".join(buff)

    def getSign(self, obj):
        """生成签名"""
        # 签名步骤一: 按字典序排序参数,formatBizQueryParaMap已做:
        String = self.formatBizQueryParaMap(obj, True)
        # 签名步骤二: 在string后加入KEY:
        StringToSign = 'GET&%2F&{}'.format(quote(String))
        # 签名步骤三: sha1加密:
        Sha1String = hmac.new('{}&'.format(self.AppSecrt).encode(), StringToSign.encode(), hashlib.sha1).digest()
        return b64encode(Sha1String).decode()

    def request_pull(self, params):
        url = 'http://cloudpush.aliyuncs.com/?'
        params['Signature'] = self.getSign(params)
        request_url = url + '{}'.format(self.formatBizQueryParaMap(params, True))
        return requests.get(request_url)

    def push_message(self, devices='', Title='', Summary='', Body=''):
        # params = self.set_parameters('4605de4f499b404c9cc7b86461c16b44')
        params = self.set_parameters(devices)
        params['Summary'] = Summary        # IOS通知内容
        params['Body'] = Body            # 安卓通知内容.
        params['Title'] = Title         # 安卓通知标题.
        result = self.request_pull(params)
        return result
