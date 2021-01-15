import logging
import requests
from django.conf import settings
from redis import StrictRedis

logger = logging.getLogger('error')


def get_data_token():
    redis = StrictRedis(settings.KV_REDIS, password=settings.KV_REDIS_PASSWORD, decode_responses=True)
    data_token = 'data_token'
    token = redis.get(data_token)
    if token:
        return token

    request_url = "{}/api/v1/auth/".format(settings.DATA_SERVICE_HOST)

    params = {
        'client_id': settings.DATA_SERVICE_ID,
        'client_secret': settings.DATA_SERVICE_SECRET,
    }
    res = requests.post(request_url, data=params, timeout=60)
    if res.ok:
        token = res.json()['token']
        if token:
            redis.set(data_token, token.encode('utf-8'), 60 * 60 * 24)
    return token


def check_black(content):
    token = get_data_token()
    if not token:
        return None

    headers = {
        'content-type': 'application/json',
        'Authorization': 'jwt {}'.format(str(token))
    }

    request_url = "{}/api/v1/rule/check_black/".format(settings.DATA_SERVICE_HOST)
    content_list = []
    for c in content:
        content_list.append({'type': c['type'], 'content': c['content']})
    data = {
        'content': content_list
    }
    res = requests.post(request_url, timeout=60, json=data, headers=headers)
    return res


def check_face_black(order_number, image):
    token = get_data_token()
    if not token:
        return None

    headers = {
        'content-type': 'application/json',
        'Authorization': 'jwt {}'.format(str(token))
    }

    request_url = "{}/api/v1/rule/check_face_black/".format(settings.DATA_SERVICE_HOST)

    data = {
        'order_number': order_number,
        'face': image
    }
    res = requests.post(request_url, timeout=60, json=data, headers=headers)
    return res


def check_outer_black(name, id_number, phone_number, order_number):
    token = get_data_token()
    if not token:
        return None

    headers = {
        'content-type': 'application/json',
        'Authorization': 'jwt {}'.format(str(token))
    }

    request_url = "{}/api/v1/rule/check_outer_black/".format(settings.DATA_SERVICE_HOST)

    data = {
        'name': name,
        'id_number': id_number,
        'phone_number': phone_number,
        'order_number': order_number
    }
    res = requests.post(request_url, timeout=60, json=data, headers=headers)
    return res


def review_result(reject, reject_reason, locked_days, order_number, step, reject_data):
    token = get_data_token()
    if not token:
        return None

    headers = {
        'content-type': 'application/json',
        'Authorization': 'jwt {}'.format(str(token))
    }

    request_url = "{}/api/v1/rule/result/".format(settings.DATA_SERVICE_HOST)

    data = {
        'reject': reject,
        'reject_reason': reject_reason,
        'locked_days': locked_days,
        'order_number': order_number,
        'step': step,
        'reject_data': reject_data
    }
    res = requests.post(request_url, timeout=60, json=data, headers=headers)
    return res
