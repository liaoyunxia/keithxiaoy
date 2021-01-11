import requests
import json
from public.utils.func_ext import headers, write_log


class MenuCreator(object):

    def __init__(self, appid=None, access_token=None):
        self.appid = appid
        self.access_token = access_token
        self.menu = {}

    def create_menu(self, menu_data):
        url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token={}'.format(self.access_token)
        result = requests.post(url, data=json.dumps(menu_data, ensure_ascii=False).encode('utf-8'), headers=headers)
        if result.status_code != 200:
            write_log('create_menu_result', 'status_code={}'.format(result.status_code))
            return False
        else:
            res = json.loads(result.text)
            write_log('create_menu_result', 'res={}'.format(res))
            if res['errmsg'] == 'ok' and res['errcode'] == 0:
                return True
            return False

    def get_menu(self):
        url = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token={}'.format(self.access_token)
        result = requests.get(url, headers=headers)
        cur_menu = {}
        if result.status_code == 200:
            cur_menu = json.loads(result.text)
            if cur_menu.get('menu', 0):
                return cur_menu
        self.menu = cur_menu
        return cur_menu
