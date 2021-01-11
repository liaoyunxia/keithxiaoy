from collections import OrderedDict
import datetime
import hashlib
import json
import random
import time
from urllib.parse import quote

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_text
from ipware.ip import get_ip
import requests
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
from rest_framework_jwt.authentication import jwt_decode_handler, \
    jwt_get_username_from_payload
from rest_framework_jwt.settings import api_settings

import syslog

from ..weixin.WXBizMsgCrypt import WxComponentConf_pub


headers = {'Content-Type': 'application/json'}


def get_header(request):
    return {'Content-Type': 'application/json', 'x-forwarded-for': get_ip(request, right_most_proxy=True)}


def write_log(method, msg):
    syslog.openlog(method, syslog.LOG_LOCAL0)
    syslog.syslog(syslog.LOG_INFO, msg)


class get_expired_time():
    def __init__(self):
        if settings.TEST_ENV:
            self.expired_time = 5 * 60
            self.offer_expired_time = 30 * 60
        else:
            self.expired_time = 2 * 60 * 60
            self.offer_expired_time = 24 * 60 * 60

    def get_enquiry_expired(self):
        return datetime.datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - self.expired_time)), '%Y-%m-%d %H:%M:%S')


def createNoncestr(chars, length=4):
    """产生随机字符串, 不长于32位"""
    strs = []
    for x in range(length):
        strs.append(chars[random.randrange(0, len(chars))])
    return ''.join(strs)


def formatBizQueryParaMap(paraMap, urlencode):
    """格式化参数，签名过程需要使用"""
    slist = sorted(paraMap)
    buff = []
    for k in slist:
        if k != 'sign':
            v = quote(paraMap[k]) if urlencode else paraMap[k]
            buff.append("{0}={1}".format(k, v))
    return "&".join(buff)


def trans_params(request):
    temp_dic = {}
    if request.user.is_authenticated():  # 判断用户是否登录.
        temp_dic['payment_account_number'] = request.user.payment_account_number
        temp_dic['user_id'] = request.user.id
        temp_dic['name'] = request.user.name
        temp_dic['phone_number'] = request.user.phone_number
        temp_dic['username'] = request.user.username
    for k, v in request.data.items():
        if k:
            temp_dic[k] = v
    for k, v in request.GET.items():
        if k:
            temp_dic[k] = v
    temp_dic['page_size'] = request.GET.get('page_size', 20)
    temp_dic['page'] = request.GET.get('page', 1)
    return temp_dic


def trans_wsgi_params(request):
    temp_dic = {}
    if request.user.is_authenticated():  # 判断用户是否登录.
        temp_dic['payment_account_number'] = request.user.payment_account_number
        temp_dic['user_id'] = request.user.id
        temp_dic['name'] = request.user.name
        temp_dic['phone_number'] = request.user.phone_number
        temp_dic['username'] = request.user.username
    return temp_dic


def get_result(count, data, next_page=None, previous_page=None):
    return OrderedDict([('count', count), ('next', next_page), ('previous', previous_page), ('results', data)])


def get_nickname(nickname):
    temp_list = []
    if len(nickname) != 0:
        for x in range(len(nickname) - 1):
            temp_list.append('*')
        return nickname[0] + ''.join(temp_list)
    return nickname


def get_username(username):
    temp_list = []
    if len(username) >= 6:
        for x in range(len(username) - 3):
            temp_list.append('*')
        return username[:2] + ''.join(temp_list) + username[-1:]
    return username


def get_financiername(name):
    temp_list = []
    if len(name) > 6:
        for x in range(len(name) - 6):
            temp_list.append('*')
        return name[:2] + ''.join(temp_list) + name[-4:]
    else:
        for x in range(len(name)):
            temp_list.append('*')
        return ''.join(temp_list)
    return name


def get_name(name):
    if name == '':
        name = '神秘人'
    temp_list = []
    if len(name) != 0:
        for x in range(len(name) - 1):
            temp_list.append('*')
        return name[0] + ''.join(temp_list)
    return name


def get_token(request):
    token = dict(('token', value) for (header, value) in request.META.items() if header == 'HTTP_AUTHORIZATION').get('token', '')
    return token


def get_jwt_value(request):
    auth = get_authorization_header(request).split()
    auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()
    if not auth or smart_text(auth[0].lower()) != auth_header_prefix:
        return None
    if len(auth) == 1:
        return None
    elif len(auth) > 2:
        return None
    return auth[1]


def get_user(jwt_value):
    payload = jwt_decode_handler(jwt_value)
    username = jwt_get_username_from_payload(payload)
    if not username:
        return None
    try:
        user = get_user_model().objects.get_by_natural_key(username)
    except get_user_model().DoesNotExist:
        return None
    return user


def jwt_check_user(request):
    jwt_value = get_jwt_value(request).decode()
    user = get_user(jwt_value)
    return user


def get_user_info(request, login_tag=True):
    token = get_token(request)
    if token != '':
        try:
            user = jwt_check_user(request)
            if not user:
                return None
        except:
            return None
    else:
        if request.user.is_authenticated():
            user = request.user
        else:
            return None
    if request.user.is_authenticated() and request.user.id != user.id:
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        # token的用户自动登录.
        auth.login(request, user)
    if not request.user.is_authenticated():
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        # token的用户自动登录.
        auth.login(request, user)
    return user


def get_app_name(request):
    app_name = dict(('app_name', value) for (header, value) in request.META.items() if header == 'HTTP_APP_SCHEME').get('app_name', '')
    return app_name


def local2utc(local_st):
    # “”“本地时间转UTC时间（-8:00）”“”
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st


def utc2local(utc_st):
    '''UTC时间转本地时间（+8:00）'''
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
    String = '{0}&key={1}'.format(String, key)
    # 签名步骤三: MD5加密:
    String = hashlib.md5(String.encode()).hexdigest()
    # 签名步骤四: 所有字符转为大写:
    result_ = String.upper()
    return result_


def get_pre_auth_code(mc, token):
    url = 'https://api.weixin.qq.com/cgi-bin/component/api_create_preauthcode?component_access_token={}'.format(token)
    data = {'component_appid': WxComponentConf_pub.APPID}
    result = requests.post(url, json.dumps(data), headers=headers).text
    write_log('pre_auth_code_result', '{}'.format(result))
    if 'pre_auth_code' in result:
        code_result = json.loads(result)
        mc.set('pre_auth_code', code_result['pre_auth_code'], code_result['expires_in'])
        return code_result['pre_auth_code']
    return None


def get_api_component_token(mc, verify_ticket):
    url = 'https://api.weixin.qq.com/cgi-bin/component/api_component_token'
    data = {'component_appid': WxComponentConf_pub.APPID,
            'component_appsecret': WxComponentConf_pub.APPSECRET,
            'component_verify_ticket': verify_ticket}
    result = requests.post(url, data=json.dumps(data), headers=headers).text
    write_log('api_component_token_result', '{}'.format(result))
    if 'component_access_token' in result:
        component_result = json.loads(result)
        mc.set('component_access_token', component_result['component_access_token'], component_result['expires_in'])
        return component_result['component_access_token']
    return None


def get_user_list(request):
    if not request.user.is_authenticated():
        return []
    elif request.user.is_authenticated() and request.user.organization.all() == []:
        return [request.user.id]
    return [item.id for item in get_user_model().objects.filter(organization__in=request.user.organization.all())]


def is_offce(request):
    if not request.user.is_authenticated():
        return False
    group_name = [item.name for item in request.user.groups.all()]
    if '营销内勤' in group_name:
        return True
    else:
        return False


def is_manager(request):
    if not request.user.is_authenticated():
        return False
    group_name = [item.name for item in request.user.groups.all()]
    if '客户经理' in group_name:
        return True
    else:
        return False


def is_financier(request):
    if not request.user.is_authenticated():
        return False
    group_name = [item.name for item in request.user.groups.all()]
    if '转贴人员' in group_name:
        return True
    else:
        return False


def BaseExceptions(message):
    ex = exceptions.APIException
    ex.status_code = 400
    ex.default_detail = message
    return ex


def is_valid_date(string):
    try:
        time.strptime(string, "%Y-%m-%d %H:%M:%S")
        return True
    except:
        return False