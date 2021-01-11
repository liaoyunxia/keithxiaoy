import time

from ..rest_framework.serializers import UserCreatedSerializer


def get_local_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def jwt_response_payload_handler(token, user=None, request=None):
    is_first = 0
    if user:
        if not user.last_login:
            is_first = 1
        user.last_login = get_local_time()
        user.save()
    return UserCreatedSerializer(user, context={'request': request, 'is_first': is_first}).data
