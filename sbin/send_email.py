from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import os.path
import smtplib
import sys
from time import sleep
import traceback
import urllib.request

import redis

from py_mysql import MysqlClient
import syslog


def write_log(method, msg):
    syslog.openlog(method, syslog.LOG_LOCAL0)
    syslog.syslog(syslog.LOG_INFO, msg)


class SendEmail():
    def __init__(self):
        self.server = 'smtpdm.aliyun.com'
        self.port = 25
        self.username = 'support@notice.cmcaifu.com'
        self.password = 'cmcaifu1234'

    def send_email_params(self, send_from, send_to, text='', urls=[]):
        self.msg = MIMEMultipart()
        self.msg['From'] = send_from
        self.msg['To'] = send_to
        self.msg['Date'] = formatdate(localtime=True)
        self.msg['Subject'] = '项目合同'
        self.msg.attach(MIMEText(text))
        for url in urls:
            part = MIMEBase('application', "octet-stream")
            response = urllib.request.urlopen(url)
            part.set_payload(response.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(url.split('?')[0])))
            self.msg.attach(part)

    def send_email(self, send_from, send_to, text='', urls=[]):
        self.send_email_params(send_from, send_to, text, urls)
        smtp = smtplib.SMTP(self.server, self.port)
        smtp.login(self.username, self.password)
        smtp.sendmail(send_from, send_to, self.msg.as_string())
        smtp.quit()


if __name__ == '__main__':
    TEST_ENV = int(sys.argv[1])
    if TEST_ENV:
        redis_client = redis.Redis(host='10.117.182.179',
                                   port=6379,
                                   db=0)
        domain_name = 'http://test.cmcaifu.com'
    else:
        redis_client = redis.Redis(host='e6837b0ac94b4118.m.cnhza.kvstore.aliyuncs.com',
                                   port=6379,
                                   db=0,
                                   password='e6837b0ac94b4118:ReO119fh1c')
        domain_name = 'https://www.cmcaifu.com'
    while True:
        try:
            queryset = redis_client.rpop('email_message_key')
            if queryset:
                queryset = eval(queryset)
                write_log('email_message', '{}'.format(queryset))
                order_id = queryset.get('order_id', '')
                token = queryset.get('token', '')
                send_to = queryset.get('send_to', '346985049@qq.com')
                download_urls = queryset.get('contract_urls', '').strip().split('\n')
                if download_urls != []:
                    SendEmail().send_email('support@notice.cmcaifu.com', send_to=send_to, text='', urls=download_urls)
            else:
                sleep(1)
        except:
            write_log('email_error', '{}'.format(traceback.format_exc(5)))
