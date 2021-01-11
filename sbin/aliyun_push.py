from base64 import b64encode
import datetime
import hashlib
import hmac
import random
from urllib.parse import quote

import requests

import syslog


now = datetime.datetime.isoformat(datetime.datetime.utcnow()).split('.')[0] + 'Z'


class ALiYunPush():
    def __init__(self):
        self.AppSecrt = 'RTwvDfFNmMGro4C3f5vaBUMwggs6dx'
        self.AppKey = '23302657'
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

    def set_parameters(self, accounts):
        parameters = {}
        parameters['RegionId'] = 'cn-hangzhou'
        parameters['Version'] = self.Version
        parameters['AccessKeyId'] = self.AccessKeyId
        parameters['SignatureMethod'] = 'HMAC-SHA1'
        parameters['SignatureVersion'] = '1.0'
        parameters['Timestamp'] = '{}'.format(self.now())
        parameters['SignatureNonce'] = self.createNoncestr(32)
        parameters['Action'] = 'Push'
        parameters['AppKey'] = self.AppKey
        parameters['Target'] = 'account'
        parameters['TargetValue'] = accounts
        parameters['Remind'] = 'true'
        parameters['StoreOffline'] = 'true'
        parameters['DeviceType'] = '3'
        parameters['Type'] = '1'
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
        # 签名步骤一：按字典序排序参数,formatBizQueryParaMap已做:
        String = self.formatBizQueryParaMap(obj, True)
        # 签名步骤二：在string后加入KEY:
        StringToSign = 'GET&%2F&{}'.format(quote(String))
        # 签名步骤三：sha1加密:
        Sha1String = hmac.new('{}&'.format(self.AppSecrt).encode(), StringToSign.encode(), hashlib.sha1).digest()
        return b64encode(Sha1String).decode()

    def request_pull(self, params):
        url = 'http://cloudpush.aliyuncs.com/?'
        params['Signature'] = self.getSign(params)
        request_url = url + '{}'.format(self.formatBizQueryParaMap(params, True))
        result = requests.get(request_url)
        self.write_log('aliyun_push_result', '{}:{}'.format(result.status_code, result.text))
        return result

    def push_message(self, accounts, Title, Summary, Body):
        params = self.set_parameters(accounts)
        params['Summary'] = Summary
        params['Body'] = Body
        params['Title'] = Title
        params['ApnsEnv'] = 'DEV'
        self.request_pull(params)

    def write_log(self, method, msg):
        syslog.openlog(method, syslog.LOG_LOCAL0)
        syslog.syslog(syslog.LOG_INFO, msg)
