from collections import OrderedDict
import datetime
import json
import random
import time
from urllib.parse import quote

from django.conf import settings
import requests
from rest_framework.response import Response

from nyssance.rest_framework.response import ResponseBadRequest
import syslog


headers = {'Content-Type': 'application/json'}


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
    if request.user.is_authenticated():   # 判断用户是否登录.
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
    return temp_dic


def get_request(request, url, method):
    write_log('{}_request'.format(method), '{}'.format(trans_params(request)))
    result = requests.post(url, data=json.dumps(trans_params(request)), headers=headers)
    response = result.text
    write_log('{}_result'.format(method), '{}'.format(response))
    if result.status_code >= 400:
        return ResponseBadRequest('{}'.format(response))
    try:
            data = json.loads(response)
            return Response(status=result.status_code, data=data)
    except:
        return ResponseBadRequest('{}'.format(response))


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
        for x in range(len(username) - 6):
            temp_list.append('*')
        return username[:3] + ''.join(temp_list) + username[-3:]
    return username