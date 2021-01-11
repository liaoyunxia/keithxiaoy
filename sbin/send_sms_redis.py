import sys
from time import sleep

import redis

from py_mysql import MysqlClient
from sms_ytx_sdk import sendTemplateSms
import syslog


def write_log(method, msg):
    syslog.openlog(method, syslog.LOG_LOCAL0)
    syslog.syslog(syslog.LOG_INFO, msg)


if __name__ == '__main__':
    TEST_ENV = int(sys.argv[1])
    if TEST_ENV:
        redis_client = redis.Redis(host='10.117.182.179',
                                   port=6379,
                                   db=0)
    else:
        redis_client = redis.Redis(host='e6837b0ac94b4118.m.cnhza.kvstore.aliyuncs.com',
                                   port=6379,
                                   db=0,
                                   password='e6837b0ac94b4118:ReO119fh1c')
    send_template_sms = sendTemplateSms()
    while True:
        queryset = redis_client.rpop('sms_queue_key')
        if queryset:
            result = eval(queryset)
            write_log('send_sms_message', '{}'.format(result))
            params = {'name': ['phone_number'],
                      'tbl': 'accounts_user',
                      'prefix': 'where id={}'.format(result.get('user_id'))
                      }
            type_dict = {1: '63766',  # 起息.
                         2: '62023',  # 流标.
                         3: '62111',
                         4: '71074',
                         5: '71628',
                         6: '72035',
                         7: '73259',
                         8: '75835',
                         9: '73516',
                         10: '73515',
                         11: '71077',
                         12: '79949',
                         13: '83414',
                         14: '84342',
                         22: '96336',
                         23: '96337',
                         25: '96546',
                         26: '98623',
                         27: '98703',
                         28: '123578',
                         29: '123579',
                         30: '123580',
                         31: '134180',
                         32: '134182',
                         33: '134185',
                         34: '140390',
                         35: '134505',
                         36: '134506',
                         37: '135904',
                         38: '155662',
                         1001: '77979'}
            try:
                if result.get('type') in [9, 10, 11, 12, 13, 38]:
                    if result.get('type') == 12:
                        data = []
                    elif result.get('type') in [13, 38]:
                        data = [result.get('product_name')]
                    else:
                        data = [result.get('product_name'), result.get('date')]
                    for item in result.get('phone_numbers', []):
                        res = send_template_sms.send_template_sms(item, data, type_dict.get(result.get('type', 1)), 'invest')
                else:
                    mysql_client = MysqlClient(TEST_ENV)
                    mysql_client.selectQuery(params)
                    query = mysql_client.getSql()
                    app_name = 'invest'
                    template_id = type_dict.get(result.get('type', 1))
                    data = [result.get('product_name', ''), str(result.get('amount', 0) / 100)]
                    if result.get('type') == 1001:
                        data = [result.get('activity', ''), result.get('prize', '')]
                        app_name = 'fabao'
                        template_id = '77979'
                    if result.get('type') == 1:
                        data = [str(result.get('amount', 0) / 100), result.get('product_name', ''), result.get('date', '')]
                    if result.get('type') == 4:
                        data = [result.get('product_name', ''), str(result.get('amount', 0) / 100), str(result.get('real_deal_amount', 0) / 100), str(result.get('refund_amount', 0) / 100)]
                    if result.get('type') in [5, 6, 7, 8]:
                        data = [result.get('code', '')]
                        if result.get('type') in [7, 8]:
                            data = [result.get('product_name', ''), result.get('code', '')]
                        app_name = 'fabao'
                    if result.get('type') == 14:
                        data = [result.get('phone_number', ''), str(result.get('amount', 0) / 100)]
                    if result.get('type') == 22:
                        data = [result.get('product_name', '')]
                    if result.get('type') == 23:
                        data = [result.get('product_name', ''), str(result.get('traded_principal', 0) / 100),
                                str(result.get('gross', 0) / 100), str(result.get('traded_gross', 0) / 100),
                                str(result.get('service_charge', 0) / 100), str(result.get('real_amount', 0) / 100)]
                    if result.get('type') == 25:
                        data = [result.get('product_name', ''), str(result.get('refund', 0) / 100)]
                    if result.get('type') in [26, 27]:
                        data = [result.get('name', ''), result.get('product_name', ''), str(result.get('amount', 0) / 100)]
                    if result.get('type') in [29, 30]:
                        data = [str(result.get('amount', 0) / 100), result.get('product_name', '')]
                    if result.get('type') in [31, 33]:
                        data = [result.get('grade', '')]
                    if result.get('type') in [32, 37]:
                        data = []
                    if result.get('type') == 34:
                        data = [result.get('invest_type'), result.get('product_name'),
                                str((result.get('rate', 0) + result.get('other_rate', 0)) / 100),
                                str(result.get('period', 0)), str(result.get('amount', 0) / 100)]
                    if result.get('type') == 35:
                        data = [result.get('product_name')]
                    if result.get('type') == 36:
                        data = [result.get('invest_type'), result.get('product_name'),
                                str(result.get('rate', 0) / 100), str(result.get('amount', 0) / 100)]
                    for item in query:
                        res = send_template_sms.send_template_sms(item.get('phone_number'), data, template_id, app_name)
                    mysql_client.close()
            except Exception as e:
                write_log('send_sms_error', '{}'.format(e))
        else:
            sleep(1)
