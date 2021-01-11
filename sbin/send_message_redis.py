import datetime
import sys
from time import sleep
import time
import traceback

import redis

from aliyun_push import ALiYunPush
from py_mysql import MysqlClient
import syslog
from trans_message import TransMessage


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
            queryset = redis_client.rpop('message_queue_key')
            if queryset:
                queryset = eval(queryset)
                write_log('send_message_redis_queryset', '{}'.format(queryset))
                if queryset['type'] == 0:
                    params = {'name': ['id'],
                              'tbl': 'accounts_user',
                              'prefix': ''
                              }
                    mysql_client_1 = MysqlClient(TEST_ENV)
                    mysql_client_1.selectQuery(params)
                    query = mysql_client_1.getSql()
                    for item in query:
                        user_key = 'user_message:{}'.format(redis_master(item['id']))
                        message_list = []
                        if redis_client.hexists(user_key, 'data:{}'.format(item['id'])):
                            message_list = eval(redis_client.hget(user_key, 'data:{}'.format(item['id'])))
                        message = {"id_str": "{}".format(generate_shard_id(item['id'])),
                                   "template_id": 0,
                                   "object_id": queryset['pk']}
                        message_list.append(message)
                        redis_client.hset(user_key, 'data:{}'.format(item['id']), message_list)
                        data_status = {}
                        if redis_client.hexists(user_key, 'data_status:{}'.format(item['id'])):
                            data_status = eval(redis_client.hget(user_key, 'data_status:{}'.format(item['id'])))
                        data_status['1'] = 1
                        redis_client.hset(user_key, 'data_status:{}'.format(item['id']), data_status)
                    mysql_client_1.close()
                else:
                    if queryset['type'] in [7, 8] and queryset.get('badges_tag') == 1:
                        for user_id in queryset['user_ids']:
                            user_key = 'user_message:{}'.format(redis_master(user_id))
                            data_status = {}
                            if redis_client.hexists(user_key, 'data_status:{}'.format(user_id)):
                                data_status = eval(redis_client.hget(user_key, 'data_status:{}'.format(user_id)))
                            data_status[str(queryset['type'])] = 1
                            redis_client.hset(user_key, 'data_status:{}'.format(user_id), data_status)
                    else:
                        user_key = 'user_message:{}'.format(redis_master(queryset['user_id']))
                        message_list = []
                        if redis_client.hexists(user_key, 'data:{}'.format(queryset['user_id'])):
                                message_list = eval(redis_client.hget(user_key, 'data:{}'.format(queryset['user_id'])))
                        message = queryset
                        message['id_str'] = "{}".format(generate_shard_id(queryset['user_id']))
                        message['template_id'] = "{}".format(queryset['type'])
                        message_list.append(message)
                        redis_client.hset(user_key, 'data:{}'.format(queryset['user_id']), message_list)
                        data_status = {}
                        if redis_client.hexists(user_key, 'data_status:{}'.format(queryset['user_id'])):
                            data_status = eval(redis_client.hget(user_key, 'data_status:{}'.format(queryset['user_id'])))
                        data_status['0'] = 1
                        redis_client.hset(user_key, 'data_status:{}'.format(queryset['user_id']), data_status)
                        if TEST_ENV:  # 只在测试环境下测试.
                            params = {'name': ['username'],
                                      'tbl': 'accounts_user',
                                      'prefix': 'where id={}'.format(queryset['user_id'])
                                      }
                            mysql_client = MysqlClient(TEST_ENV)
                            mysql_client.selectQuery(params)
                            query = mysql_client.getSql()
                            for item in query:
                                ap = ALiYunPush()
                                message = TransMessage(queryset, '', TEST_ENV).trans_message()
                                ap.push_message(item['username'], message['title'], message['content'], message['content'])
                            mysql_client.close()
            else:
                sleep(1)
        except:
            write_log('send_message_error', '{}'.format(traceback.format_exc(5)))
