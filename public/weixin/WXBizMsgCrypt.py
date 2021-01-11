
""" 对公众平台发送给公众账号的消息加解密示例代码.
@copyright: Copyright (c) 1998-2014 Tencent Inc.

"""
# ------------------------------------------------------------------------
"""
关于Crypto.Cipher模块，ImportError: No module named 'Crypto'解决方案
请到官方网站 https://www.dlitz.net/software/pycrypto/ 下载pycrypto。
下载后，按照README中的“Installation”小节的提示进行pycrypto安装。
"""

import base64
import hashlib
import json
import os
import random
import socket
import struct
import time
import traceback
from urllib.parse import quote

from Crypto.Cipher import AES
import requests

import xml.etree.cElementTree as ET


class WxComponentConf_pub(object):
    """配置账号信息"""
    CURL_TIMEOUT = 30
    HTTP_CLIENT = "CURL"  # ("URLLIB", "CURL")

    # 微信配置:
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    NOTIFY_URL = "http://wxpay.weixin.qq.com/pub_v2/pay/notify.v2.php"
    APPID = "wxf75f10dc5c1d4356"
    APPSECRET = "5d7151b8d3f636672ea648639ad54435"
    APPTOKEN = 'Qodome2016'
    APPAESKey = 'XChQlGSS17vITnedtQ03nyYQZi1FWdO03dDvKbWR123'
    MCHID = "10026243"
    KEY = "jfdsai789FASIOIJOJFDS54355324fds"
    SSLCERT_PATH = "{}/weixin/cacert/test/apiclient_cert.pem".format(BASE_PATH)
    SSLKEY_PATH = "{}/weixin/cacert/test/apiclient_key.pem".format(BASE_PATH)


class FormatException(Exception):
    pass


def throw_exception(message, exception_class=FormatException):
    """my define raise exception function"""
    raise exception_class(message)


class SHA1:
    """计算公众平台的消息签名接口"""

    def getSHA1(self, token, timestamp, nonce, encrypt):
        """用SHA1算法生成安全签名
        @param token:  票据.
        @param timestamp: 时间戳.
        @param encrypt: 密文.
        @param nonce: 随机字符串.
        @return: 安全签名.
        """
        try:
            sortlist = [token, timestamp, nonce, encrypt]
            sortlist.sort()
            sha = hashlib.sha1()
            sha.update("".join(sortlist))
            return 0, sha.hexdigest()
        except:
            traceback.print_exc(5)
            return -1, None


class XMLParse:
    """提供提取消息格式中的密文及生成回复消息格式的接口"""

    # xml消息模板
    AES_TEXT_RESPONSE_TEMPLATE = """<xml>
<Encrypt><![CDATA[%(msg_encrypt)s]]></Encrypt>
<MsgSignature><![CDATA[%(msg_signaturet)s]]></MsgSignature>
<TimeStamp>%(timestamp)s</TimeStamp>
<Nonce><![CDATA[%(nonce)s]]></Nonce>
</xml>"""

    def extract(self, xmltext):
        """提取出xml数据包中的加密消息
        @param xmltext: 待提取的xml字符串
        @return: 提取出的加密消息字符串.
        """
        try:
            xml_tree = ET.fromstring(xmltext)
            encrypt = xml_tree.find("Encrypt")
            touser_name = xml_tree.find("ToUserName")
            return 0, encrypt.text, touser_name.text
        except:
            return -1, None, None

    def generate(self, encrypt, signature, timestamp, nonce):
        """生成xml消息
        @param encrypt: 加密后的消息密文.
        @param signature: 安全签名.
        @param timestamp: 时间戳.
        @param nonce: 随机字符串.
        @return: 生成的xml字符串.
        """
        resp_dict = {'msg_encrypt': encrypt,
                     'msg_signaturet': signature,
                     'timestamp': timestamp,
                     'nonce': nonce
                     }
        resp_xml = self.AES_TEXT_RESPONSE_TEMPLATE % resp_dict
        return resp_xml


class PKCS7Encoder():
    """提供基于PKCS7算法的加解密接口"""

    block_size = 32

    def encode(self, text):
        """ 对需要加密的明文进行填充补位.
        @param text: 需要进行填充补位操作的明文.
        @return: 补齐明文字符串.
        """
        text_length = len(text)
        # 计算需要填充的位数.
        amount_to_pad = self.block_size - (text_length % self.block_size)
        if amount_to_pad == 0:
            amount_to_pad = self.block_size
        # 获得补位所用的字符.
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    def decode(self, decrypted):
        """删除解密后明文的补位字符
        @param decrypted: 解密后的明文.
        @return: 删除补位字符后的明文.
        """
        pad = ord(decrypted[-1])
        if pad < 1 or pad > 32:
            pad = 0
        return decrypted[:-pad]


class Prpcrypt(object):
    """提供接收和推送给公众平台消息的加解密接口"""

    def __init__(self, key):
        self.key = key
        # 设置加解密模式为AES的CBC模式
        self.mode = AES.MODE_CBC

    def encrypt(self, text, appid):
        """对明文进行加密
        @param text: 需要加密的明文.
        @return: 加密得到的字符串.
        """
        # 16位随机字符串添加到明文开头
        text = self.get_random_str() + struct.pack("I", socket.htonl(len(text))) + text + appid
        # 使用自定义的填充方式对明文进行补位填充.
        pkcs7 = PKCS7Encoder()
        text = pkcs7.encode(text)
        # 加密.
        cryptor = AES.new(self.key, self.mode, self.key[:16])
        try:
            ciphertext = cryptor.encrypt(text)
            # 使用BASE64对加密后的字符串进行编码
            return 0, base64.b64encode(ciphertext)
        except:
            return -1, None

    def decrypt(self, text, appid):
        """对解密后的明文进行补位删除
        @param text: 密文.
        @return: 删除填充补位后的明文.
        """
        try:
            cryptor = AES.new(self.key, self.mode, self.key[:16])
            # 使用BASE64对密文进行解码，然后AES-CBC解密
            plain_text = cryptor.decrypt(base64.b64decode(text)).decode()
        except:
            traceback.print_exc(5)
            return -1, None
        try:
            pad = ord(plain_text[-1])
            # 去掉补位字符串.
            # 去除16位随机字符串
            content = plain_text[16:-pad]
            return 0, self.xmlToArray(self.txt_wrap_by('<xml>', '</xml>', content))
        except:
            traceback.print_exc(5)
            return -1, None
        return 0, 'xml_content'

    def get_random_str(self, length=16):
        """ 随机生成16位字符串
        @return: 16位字符串
        """
        chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
        strs = []
        for x in range(length):
            strs.append(chars[random.randrange(0, len(chars))])
        return "".join(strs)

    def xmlToArray(self, xml):
        """将xml转为array"""
        array_data = {}
        root = ET.fromstring(xml)
        for child in root:
            value = child.text
            array_data[child.tag] = value
        return array_data

    def txt_wrap_by(self, start_str, end, html):
        start = html.find(start_str)
        if start > 0:
            start += len(start_str)
            end = html.find(end, start)
            if end > 0:
                return '<xml>' + html[start:end].strip() + '</xml>'


class WXBizMsgCrypt(object):
    #构造函数
    # @param sToken: 公众平台上，开发者设置的Token。
    # @param sEncodingAESKey: 公众平台上，开发者设置的EncodingAESKey
    # @param sAppId: 企业号的AppId
    def __init__(self):
        try:
            self.key = base64.b64decode(WxComponentConf_pub.APPAESKey + "=")
            assert len(self.key) == 32
        except:
            throw_exception("[error]: EncodingAESKey unvalid !", FormatException)
        self.token = WxComponentConf_pub.APPTOKEN
        self.appid = WxComponentConf_pub.APPID

    def EncryptMsg(self, sReplyMsg, sNonce, timestamp=None):
        #将公众号回复用户的消息加密打包
        # @param sReplyMsg: 企业号待回复用户的消息，xml格式的字符串
        # @param sTimeStamp: 时间戳，可以自己生成，也可以用URL参数的timestamp,如为None则自动用当前时间
        # @param sNonce: 随机串，可以自己生成，也可以用URL参数的nonce
        # sEncryptMsg: 加密后的可以直接回复用户的密文，包括msg_signature, timestamp, nonce, encrypt的xml格式的字符串,
        # return：成功0，sEncryptMsg,失败返回对应的错误码None
        pc = Prpcrypt(self.key)
        ret, encrypt = pc.encrypt(sReplyMsg, self.appid)
        if ret != 0:
            return ret, None
        if timestamp is None:
            timestamp = str(int(time.time()))
        # 生成安全签名.
        sha1 = SHA1()
        ret, signature = sha1.getSHA1(self.token, timestamp, sNonce, encrypt)
        if ret != 0:
            return ret, None
        xmlParse = XMLParse()
        return ret, xmlParse.generate(encrypt, signature, timestamp, sNonce)

    def DecryptMsg(self, encrypt):
        # 检验消息的真实性，并且获取解密后的明文.
        # @param sMsgSignature: 签名串，对应URL参数的msg_signature
        # @param sTimeStamp: 时间戳，对应URL参数的timestamp
        # @param sNonce: 随机串，对应URL参数的nonce
        # @param sPostData: 密文，对应POST请求的数据
        #  xml_content: 解密后的原文，当return返回0时有效
        # @return: 成功0，失败返回对应的错误码
        # 验证安全签名.
        pc = Prpcrypt(self.key)
        ret, xml_content = pc.decrypt(encrypt, self.appid)
        return ret, xml_content

    def xmlToArray(self, xml):
        """将xml转为array"""
        array_data = {}
        root = ET.fromstring(xml)
        for child in root:
            value = child.text
            array_data[child.tag] = value
        return array_data


class Common_util_pub(object):
    """所有接口的基类"""

    def trimString(self, value):
        if value is not None and len(value) == 0:
            value = None
        return value

    def createNoncestr(self, length=32):
        """产生随机字符串，不长于32位"""
        chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
        strs = []
        for x in range(length):
            strs.append(chars[random.randrange(0, len(chars))])
        return "".join(strs)

    def formatBizQueryParaMap(self, paraMap, urlencode):
        """格式化参数，签名过程需要使用"""
        slist = sorted(paraMap)
        buff = []
        for k in slist:
            v = quote(paraMap[k]) if urlencode else paraMap[k]
            buff.append("{0}={1}".format(k, v))

        return "&".join(buff)

    def formatBizQueryParaMapNotSort(self, paraMap, urlencode):
        """无需排序，组成访问参数"""
        buff = []
        for k, v in paraMap.items():
            v = quote(v) if urlencode else v
            buff.append("{0}={1}".format(k, v))
        return "&".join(buff)

    def getSign(self, obj):
        """生成签名"""
        # 签名步骤一：按字典序排序参数,formatBizQueryParaMap已做:
        String = self.formatBizQueryParaMap(obj, False)
        # 签名步骤二：在string后加入KEY:
        String = "{0}&key={1}".format(String, WxComponentConf_pub.KEY)
        # 签名步骤三：MD5加密:
        String = hashlib.md5(String.encode()).hexdigest()
        # 签名步骤四：所有字符转为大写:
        result_ = String.upper()
        return result_

    def arrayToXml(self, arr):
        """array转xml"""
        keylist = sorted(arr)
        xml = ["<xml>"]
        for k in keylist:
            if k != 'sign':
                xml.append("<{0}>{1}</{0}>".format(k, arr[k]))
#             if v.isdigit():
#                 xml.append("<{0}>{1}</{0}>".format(k, v))
#             else:
#                 xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
        xml.append("<sign>{}</sign>".format(arr['sign']))
        xml.append("</xml>")
        return "".join(xml)

    def xmlToArray(self, xml):
        """将xml转为array"""
        array_data = {}
        root = ET.fromstring(xml)
        for child in root:
            value = child.text
            array_data[child.tag] = value
        return array_data


class WxComponent_pub(Common_util_pub):
    """JSAPI支付——H5网页端调起支付接口"""
    code = None  # code码，用以获取openid:
    openid = None  # 用户的openid:
    parameters = None  # jsapi参数，格式为json:
    prepay_id = None  # 使用统一支付接口得到的预支付id:
    curl_timeout = None  # curl超时时间:

    def __init__(self, timeout=WxComponentConf_pub.CURL_TIMEOUT):
        self.curl_timeout = timeout
        self.wx_parameters = {}  # 请求参数，类型为关联数组.
        self.result = {}  # 返回参数，类型为关联数组.

    def setWxParameter(self, parameter, parameterValue):
        """设置请求参数"""
        self.wx_parameters[self.trimString(parameter)] = self.trimString(parameterValue)

    def createOauthUrlForAuthCode(self, redirectUrl):
        """生成可以获得code的url"""
        urlObj = {}
        urlObj["component_appid"] = WxComponentConf_pub.APPID
        urlObj["pre_auth_code"] = self.wx_parameters['pre_auth_code']
        urlObj['redirect_uri'] = quote(redirectUrl, '')
        bizString = self.formatBizQueryParaMap(urlObj, False)
        return "https://mp.weixin.qq.com/cgi-bin/componentloginpage?" + bizString

    def createOauthUrlForCode(self, redirectUrl):
        bizString = ''
        bizString += 'appid={}&'.format(self.wx_parameters['app_id'])
        bizString += 'redirect_uri={}&'.format(quote('{}?appid={}'.format(redirectUrl, self.wx_parameters['app_id']), ''))
        bizString += 'response_type=code&'
        bizString += 'scope=snsapi_base&'
        bizString += 'state=STATE&'
        bizString += 'component_appid={}&#wechat_redirect'.format(WxComponentConf_pub.APPID)
        return "https://open.weixin.qq.com/connect/oauth2/authorize?{}".format(bizString)

    def createOauthUrlForAccessToken(self):
        urlObj = {}
        urlObj["appid"] = self.wx_parameters['app_id']
        urlObj["code"] = self.code
        urlObj["grant_type"] = 'authorization_code'
        urlObj["component_appid"] = WxComponentConf_pub.APPID
        urlObj["component_access_token"] = self.wx_parameters['component_access_token']
        bizString = self.formatBizQueryParaMap(urlObj, False)
        return "https://api.weixin.qq.com/sns/oauth2/component/access_token?" + bizString

    def getOpenid(self):
        """通过curl向微信提交code，以获取openid"""
        url = self.createOauthUrlForAccessToken()
        data = requests.get(url).text
        if 'openid' in data:
            self.openid = json.loads(data)["openid"]
        else:
            self.openid = None
        return self.openid

    def setCode(self, code):
        """设置code"""
        self.code = code
