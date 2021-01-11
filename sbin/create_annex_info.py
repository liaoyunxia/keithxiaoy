import datetime
import json
import locale
import os
import subprocess
import sys
from time import sleep
import time

import pdfkit
import redis
import requests

from py_mysql import MysqlClient
import syslog


def write_log(method, msg):
    syslog.openlog(method, syslog.LOG_LOCAL0)
    syslog.syslog(syslog.LOG_INFO, msg)


def redis_master(user_id=None):
    if not user_id:
        return 0
    else:
        if user_id < 10000:
            return 0
        else:
            return int(user_id / 1000)


def timestamp(date):
    return time.mktime(date.timetuple())


def generate_shard_id(user_id):
    time_offset = int(timestamp(datetime.datetime.now()) - 1425168000)  # 2015-03-01 00:00:00
    return user_id | time_offset << 32


def format_currency(amount):
    price = amount / 100
    locale.setlocale(locale.LC_ALL, '')
    formatted = locale.currency(price, symbol=False, grouping=True)
    return formatted


def get_date_str(time_string):
    return time_string.split('T')[0] if time_string != '' else time_string


type_dict = {1: '发票签收单',
             2: '利息表',
             3: '内部核票', 5: '咨询服务合同',
             6: '商业汇票贴现总协议', 7: '贴现凭证', 8: '业务审查表',
             9: '业务审批表', 10: '用款申请单', 11: '应收款转让清单',
             12: '应收款登记协议', 13: '有追索权国内保理合同'}

child_type_dict = {1: '电子票据', 2: '纸质票据'}

name_dict = {1: 'invoice_sign',
             2: 'interest_table',
             3: 'ticket_file',
             5: 'collection_agreement',
             6: 'discount_agreement',
             7: 'discounting_voucher',
             8: 'investigate_table',
             9: 'approve_table',
             10: 'payment_requisition',
             11: 'receivable_inventory',
             12: 'receivable_registration_agreement',
             13: 'factor_contract'}


def trans_msg(html_str, data):
    html_string = html_str.replace('${financier_name}', data['bill']['financier']['name'])
    html_string = html_string.replace('${financier_credit_limit}', '{}'.format(format_currency(data['bill']['financier']['credit_limit'])))
    html_string = html_string.replace('${financier_business_address}', '{}'.format(data['bill']['financier']['register_address']))
    html_string = html_string.replace('${financier_postal_code}', '{}'.format(data['bill']['financier']['postal_code']))
    html_string = html_string.replace('${financier_legal_representative}', '{}'.format(data['bill']['financier']['legal_representative']))
    html_string = html_string.replace('${finanicer_fax}', '{}'.format(data['bill']['financier']['fax_code']))
    html_string = html_string.replace('${finanicer_phone_number}', '{}'.format(data['bill']['financier']['phone_number']))
    html_string = html_string.replace('${financier_contacts}', '{}'.format(','.join(item.name for item in data['bill']['financier']['contacts']['results'])))
    html_string = html_string.replace('${financier_contace_fax}', '{}'.format(','.join(item.fax_code for item in data['bill']['financier']['contacts']['results'])))
    html_string = html_string.replace('${finanicer_contace_phone_number}', '{}'.format(','.join(item.phone_number for item in data['bill']['financier']['contacts']['results'])))
    html_string = html_string.replace('${manager_name}', data['user']['name'])
    html_string = html_string.replace('${manager_organization}', '{}'.format(','.join(item.name for item in data['bill']['organizations']['results'])))
    html_string = html_string.replace('${manager_business_address}', '{}'.format(','.join(item.business_address for item in data['bill']['organizations']['results'])))
    html_string = html_string.replace('${manager_postal_code}', '{}'.format(','.join(item.postal_code for item in data['bill']['organizations']['results'])))
    html_string = html_string.replace('${manager_legal_representative}', '{}'.format(','.join(item.legal_representative for item in data['bill']['organizations']['results'])))
    html_string = html_string.replace('${manager_fax}', '{}'.format(','.join(item.fax_code for item in data['bill']['organizations']['results'])))
    html_string = html_string.replace('${manager_phone_number}', '{}'.format(','.join(item.phone_number for item in data['bill']['organizations']['results'])))
    html_string = html_string.replace('${manager_contacts}', '{}'.format(','.join(item.contact_name for item in data['bill']['organizations']['results'])))
    html_string = html_string.replace('${manager_contact_fax}', '{}'.format(','.join(item.fax_code for item in data['bill']['organizations']['results'])))
    html_string = html_string.replace('${manager_contact_phone_number}', '{}'.format(','.join(item.phone_number for item in data['bill']['organizations']['results'])))
    html_string = html_string.replace('${effective_date}', get_date_str(data['bill']['contract'].get('valid_start_date', '')))
    html_string = html_string.replace('${expiration_date}', get_date_str(data['bill']['contract'].get('valid_end_date', '')))
    html_string = html_string.replace('${factor_sign_date}', get_date_str(data['bill']['contract'].get('sign_date', '')))
    html_string = html_string.replace('${factor_sign_address}', get_date_str(data['bill']['contract'].get('sign_address', '')))
    html_string = html_string.replace('${number}', data['bill']['contract_number'])
    html_string = html_string.replace('${drawer_name}', data['bill']['drawer']['name'])
    html_string = html_string.replace('${business_type}', data['bill']['drawer']['name'])
    
    html_string = html_string.replace('${code}', data['code'])
    html_string = html_string.replace('${contract_code}', data['code'] + data['bill']['contract_number'])
    html_string = html_string.replace('${manager_phone_number}', data['user']['username'])
    html_string = html_string.replace('${sign_time}', get_date_str(data['bill'].get('loan_time', {}).get('signature_time', '')))
    html_string = html_string.replace('${start_time}', get_date_str(data['bill'].get('loan_time', {}).get('start_time', '')))
    html_string = html_string.replace('${end_time}', get_date_str(data['bill'].get('loan_time', {}).get('end_time', '')))
    html_string = html_string.replace('${pay_value}', '{}'.format(format_currency(int(data['bill']['pay_value']))))
    html_string = html_string.replace('${credit_limit}', '{}'.format(format_currency(data['bill']['financier']['credit_limit'])))
    html_string = html_string.replace('${quote_rate}', '{}%'.format(int(data['bill']['quote_rate']) / 100))
    html_string = html_string.replace('${financier_name}', data['bill']['financier']['name'])
    html_string = html_string.replace('${qualification}', data['bill']['financier']['qualification'])
    html_string = html_string.replace('${legal_representative}', data['bill']['financier']['legal_representative'])
    html_string = html_string.replace('${postal_code}', data['bill']['financier']['postal_code'])
    html_string = html_string.replace('${discount_time}', get_date_str(data['bill']['discount_time']))
    html_string = html_string.replace('${maturity_time}', get_date_str(data['bill']['maturity_time']))
    html_string = html_string.replace('${draw_time}', get_date_str(data['bill']['draw_time']))
    html_string = html_string.replace('${period}', '{}'.format(data['bill']['period']))
    html_string = html_string.replace('${bill_child_type}', child_type_dict.get(data['bill']['bill_child_type']))
    html_string = html_string.replace('${interest}', '{}'.format(format_currency(data['bill']['interest'])))
    html_string = html_string.replace('${prepayment_amount}', '{}'.format(format_currency(data['bill']['prepayment_amount'])))
    html_string = html_string.replace('${operating_expense}', '{}'.format(format_currency(data['bill']['operating_expense'])))
    html_string = html_string.replace('${operating_expense_rate}', '{}%'.format(int(data['bill']['operating_expense_rate']) / 100))
    html_string = '<head><meta charset="UTF-8"></head>' + html_string
    options = {'dpi': 250}
    wkhtmltopdf = subprocess.Popen(['which', 'wkhtmltopdf'], stdout=subprocess.PIPE).communicate()[0].strip()
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf.decode())
    pdfkit.from_string(html_string, '/tmp/out.pdf', configuration=config, options=options)


def upload_file(out_path, file_name):
    bucket_static = 'test-cloud-cmcaifu-com'
    params_url = 'http://factor.cmcaifu.com/upload_params/{}/?filename={}&bucket={}'.format('oss', file_name, bucket_static)
    data = requests.get(params_url).text
    write_log('annex_upload_data', '{}'.format(data))
    url = 'http://{}'.format(bucket_static.replace('-', '.'))  # 阿里云bucket名中不能出现.号
    response = requests.post(url, files={'file': open(out_path, 'rb')}, data=json.loads(data))
    if 200 < response.status_code < 300:
        data = json.loads(data)
        return data['domain'] + data['key']
    return ''


def get_insert_sql(bill_id, name, url):
    sql = 'insert into annex_annex (`bill_id`, `{}`) values ({}, "{}") ON DUPLICATE KEY UPDATE  {}="{}";'.format(name, bill_id, url, name, url)
    return sql


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
    while True:
        try:
            queryset = redis_client.rpop('annex_data_message')
            if queryset:
                data = json.loads(queryset.decode())
                write_log('annex_data', '{}'.format(data))
                params = {'name': ['content', 'type'],
                          'tbl': 'annex_annextemplate',
                          'prefix': ''
                          }
                mysql_client = MysqlClient(TEST_ENV)
                mysql_client.selectQuery(params)
                query = mysql_client.getSql()
                for item in query:
                    if item.get('type') in type_dict:
                        if item.get('content', '') != '':
                            trans_msg(item.get('content'), data)
                            if os.path.exists('/tmp/out.pdf'):
                                static_url = upload_file('/tmp/out.pdf', 'upload/factoring/{}/{}.pdf'.format(data.get('id'), type_dict.get(item.get('type'))))
                                write_log('annex_static_url', '{}'.format(static_url))
                                if static_url != '':
                                    insert_sql = get_insert_sql(data['bill']['id'], name_dict.get(item.get('type')), static_url)
                                    write_log('annex_insert_sql', '{}'.format(insert_sql))
                                    mysql_client.query(insert_sql)
                                sleep(1)
                mysql_client.close()
        except Exception as e:
            write_log('annex_info_error', '{}'.format(e))
