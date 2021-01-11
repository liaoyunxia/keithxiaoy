import json
import time

from django.conf import settings
import pylibmc
import requests

from .get_sign import WxPayConf_pub
from .wx_jssdk import WX_JSSDK


class PushWechatMessage():
    def __init__(self):
        self.mc = pylibmc.Client([settings.CACHES['default']['LOCATION']])
        self.api_ticket_key = '{}_api_ticket'.format(WxPayConf_pub().APPID)

    def send_message(self, open_id, title, content, order_id):
        if open_id != '':
            access_token = WX_JSSDK().get_access_token()
            template_id = 'BhteSeDaxfRVV9VZ0nz1UWFSg0j7_zVZprOGlXCAqkw'
            message_data = self.get_message(title, content)
            url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)
            redirect_url = '{}/{}'.format(settings.BASE_URL, 'wx_redirect/?order_id={}'.format(order_id))
            data = {'touser': open_id, 'template_id': template_id, 'url': redirect_url, 'data': message_data}
            requests.post(url, data=json.dumps(data))

    def get_message(self, title, content):
        data = {}
        data['first'] = {'value': title, 'color': '#173177'}
        data['keyword1'] = {'value': content, 'color': '#173177'}
        data['keyword2'] = {'value': time.strftime('%Y年%m月%d日', time.localtime(time.time())), 'color': '#173177'}
        data['remark'] = {'value': ''}
        return data
