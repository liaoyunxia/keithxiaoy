from base64 import b64encode
import datetime
import hashlib
import hmac
import time
from urllib.parse import quote

import requests


now = datetime.datetime.isoformat(datetime.datetime.utcnow()).split('.')[0] + 'Z'
AppSecrt = 'RTwvDfFNmMGro4C3f5vaBUMwggs6dx'


Pub_params = {
    'Version': '2015-11-23',
    'AccessKeyId': 'SdXIxSdYn0JtVaQv',
    'SignatureMethod': 'HMAC-SHA1',
    'Timestamp': '{}'.format(now),
    'SignatureVersion': '1.0',
    'SignatureNonce': '{}'.format(int(time.time())),
}


Single_params = {
    # 'Version': '2015-11-23',
    # 'AccessKeyId': 'SdXIxSdYn0JtVaQv',
    # 'SignatureMethod': 'HMAC-SHA1',
    # 'Timestamp': '{}'.format(now),
    # 'SignatureVersion': '1.0',
    # 'SignatureNonce': '{}'.format(int(time.time())),
    'Action': 'SingleSendMail',
    'AccountName': 'services@notice.cmcaifu.com',
    'ReplyToAddress': 'true',
    'AddressType': '0',
    'ToAddress': 'liushuo@fhic.com',
    'Subject': 'test',
    'TextBody': 'testbody',
}

Batch_params = {
    'Action': 'BatchSendMail',
    'AccountName': 'kf@notice.cmcaifu.com',
    'AddressType': '0',
    'TemplateName': 'inside',
    'ReceiversName': 'inside',
    'TagName': 'inside'
}


def formatBizQueryParaMap(paraMap, urlencode):
    """格式化参数，签名过程需要使用"""
    slist = sorted(paraMap)
    buff = []
    for k in slist:
        v = quote(paraMap[k]) if urlencode else paraMap[k]
        buff.append("{0}={1}".format(k, v))
    return "&".join(buff)


def getSign(obj):
    """生成签名"""
    # 签名步骤一: 按字典序排序参数,formatBizQueryParaMap已做:
    String = formatBizQueryParaMap(obj, True)
    print(String)
    # 签名步骤二: 在string后加入KEY:
    StringToSign = 'GET&%2F&{}'.format(quote(String))
    print(StringToSign)
    # 签名步骤三: sha1加密:
    Sha1String = hmac.new('{}&'.format(AppSecrt).encode(), StringToSign.encode(), hashlib.sha1).digest()
    return b64encode(Sha1String).decode()


# 单一发信接口.
def request_single(ToAddress, subject, TextBody):
    all_params = dict(Pub_params, ** Single_params)
    url = 'https://dm.aliyuncs.com/?'
    params = all_params
    params['ToAddress'] = ToAddress
    params['Subject'] = subject
    params['TextBody'] = TextBody
    params['Signature'] = getSign(params)
    request_url = url + '{}'.format(formatBizQueryParaMap(params, True))
    print(request_url)
    result = requests.get(request_url)
    print(result.status_code)
    print(result.text)


# 批量发信接口.
def request_Batch(ReceiversName, TemplateName, TagName):
    all_params = dict(Pub_params, ** Batch_params)
    url = 'https://dm.aliyuncs.com/?'
    params = all_params
    params['ReceiversName'] = ReceiversName
    params['TemplateName'] = TemplateName
    params['TagName'] = TagName
    params['Signature'] = getSign(params)
    request_url = url + '{}'.format(formatBizQueryParaMap(params, True))
    print(request_url)
    result = requests.get(request_url)
    print(result.status_code)
    print(result.text)


# request_single('liushuo@cmcaifu.com,wanghuidong@cmcaifu.com,liushuo@fhic.com','主题','内容')
request_Batch('inside', 'inside', 'inside')

# request_single(收件人,主题,内容)
