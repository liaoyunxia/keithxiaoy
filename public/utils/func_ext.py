import datetime
import hashlib
import mimetypes
import random
import syslog
import time
from urllib.parse import quote

from django.conf import settings
from ipware.ip import get_ip

headers = {'Content-Type': 'application/json'}


def get_header(request):
    return {'Content-Type': 'application/json', 'x-forwarded-for': get_ip(request, right_most_proxy=True)}


def write_log(method, msg):
    syslog.openlog(method, syslog.LOG_LOCAL0)
    syslog.syslog(syslog.LOG_INFO, msg)

def write_file(path, text, is_macros=True):
    """将代码写入文件"""

    STR_NOTICE = 'AUTO-GENERATED FILE. DO NOT MODIFY.'

    FILE_HEADER_PY = '# {}\n'.format(STR_NOTICE)
    FILE_HEADER_HTML = '<!-- {} -->\n'.format(STR_NOTICE)

    with open(path, 'w') as file:
        if is_macros:  # 写FILEHEADER
            content_type = mimetypes.guess_type(path)[0]
            if content_type == 'text/x-python':
                file.write(FILE_HEADER_PY)
            elif content_type == 'text/html':
                file.write(FILE_HEADER_HTML)
        # 写内容
        file.write(text)


class get_expired_time():

    def __init__(self):
        if settings.ENV == settings.STAGE.PROD:
            self.expired_time = 2 * 60 * 60
            self.offer_expired_time = 24 * 60 * 60
        else:
            self.expired_time = 5 * 60
            self.offer_expired_time = 30 * 60

    def get_enquiry_expired(self):
        return datetime.datetime.strptime(
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - self.expired_time)), '%Y-%m-%d %H:%M:%S')


def create_nonce_string(chars, length=4):
    """产生随机字符串, 不长于32位"""
    strings = []
    for x in range(length):
        strings.append(chars[random.randrange(0, len(chars))])
    return ''.join(strings)


def formatBizQueryParaMap(paraMap, urlencode):
    """格式化参数，签名过程需要使用"""
    slist = sorted(paraMap)
    buff = []
    for k in slist:
        if k != 'sign':
            v = quote(paraMap[k]) if urlencode else paraMap[k]
            buff.append('{}={}'.format(k, v))
    return '&'.join(buff)


def local2utc(local_st):
    # """本地时间转UTC时间（-8:00）"""
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st


def utc2local(utc_st):
    """UTC时间转本地时间（+8:00）"""
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st


def getSign(obj, key):
    """生成签名"""
    # 签名步骤一: 按字典序排序参数,formatBizQueryParaMap已做:
    String = formatBizQueryParaMap(obj, False)
    # 签名步骤二: 在string后加入KEY:
    String = '{}&key={}'.format(String, key)
    # 签名步骤三: MD5加密:
    String = hashlib.md5(String.encode()).hexdigest()
    # 签名步骤四: 所有字符转为大写:
    result_ = String.upper()
    return result_

def createFilename(userid, number=0, content_type='.jpg'):
    tn = str(int(time.time() * 1000)) + str(userid).zfill(4) + str(number) + content_type
    return tn

def create_filename(content_type='.jpg'):
    filename = str(int(time.time() * 1000)) + str(random.randint(10, 99)) + content_type
    return filename