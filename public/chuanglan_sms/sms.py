# -*- coding:utf-8 -*-
import logging
import requests
import json
from django.conf import settings

logger = logging.getLogger('django')


class Chuanglan_Sms():
    def __init__(self, account=None, password=None, sms_send_url=None, balance_url=None):
        self.GET_BALANCE_URL = balance_url if balance_url else settings.CHUANGLAN_BALANCE_GET_URL
        self.SMS_SEND_URL = sms_send_url if sms_send_url else settings.CHUANGLAN_SMS_SEND_URL
        self.ACCOUNT = account if account else settings.CHUANGLAN_ACCOUNT
        self.PASSWORD = password if password else settings.CHUANGLAN_PASSWORD

    def set_get_balance_parameters(self):
        params = {
            'account': self.ACCOUNT,
            'password': self.PASSWORD,
        }
        return params

    def set_sms_send_parameters(self, msg, mobile):
        params = {
            'account': self.ACCOUNT,
            'password': self.PASSWORD,
            'msg': msg,
            'mobile': mobile,
        }
        return params

    def set_voice_sms_send_parameters_1(self, intro, code, outro, mobile):
        # start_index = mobile.index('8')

        params = {
            'account': self.ACCOUNT,
            'password': self.PASSWORD,
            'intro': intro,
            'code': code,
            'outro': outro,
            'mobile': mobile,
        }
        return params

    def set_voice_sms_send_parameters(self, code, mobile):

        params = {
            'account': self.ACCOUNT,
            'password': self.PASSWORD,
            'msg': code,
            'mobile': mobile,
            'uid': '',
            'senderId': '',
        }
        return params

    def get_balance(self):
        params = self.set_get_balance_parameters()
        data = json.dumps(params)
        return requests.post(self.GET_BALANCE_URL, data=data, timeout=60)

    def send_sms(self, msg, mobile):
        params = self.set_sms_send_parameters(msg, mobile)
        data = json.dumps(params)
        return requests.post(self.SMS_SEND_URL, data=data, timeout=60)

    def send_voice_sms(self, code, mobile):
        params = self.set_voice_sms_send_parameters(code, mobile)
        data = json.dumps(params)
        logger.info('chuanglan_send_voice_sms:url={}, data={}'.format(self.SMS_SEND_URL, data))
        return requests.post(self.SMS_SEND_URL, data=data, timeout=60)
