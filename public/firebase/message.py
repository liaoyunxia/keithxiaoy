import logging
import traceback
import json
import requests
import firebase_admin
from django.conf import settings
from firebase_admin import credentials, messaging

# from public.utils.func_ext import write_log
# cred = credentials.Certificate(settings.BASE_DIR + '/public/firebase/kartu-uang-firebase.json')
# default_app = firebase_admin.initialize_app(cred)

logger = logging.getLogger(__name__)
third_logger = logging.getLogger('third')



app_dict = {
}

for channel in settings.FIREBASE_CHANNELS:
    app = firebase_admin.initialize_app(
        credentials.Certificate(settings.BASE_DIR + '/configs/firebase/{}-firebase.json'.format(channel)),
        name=channel)
    app_dict[channel] = app


class FireBase_Message():

    def __init__(self, app):
        if app in app_dict:
            self.APP = app_dict[app]
        else:
            self.APP = None

    def send_to_token_url(self, token, title, body, data={}):

        token_obj = self.APP._credential.get_access_token()

        headers = {
            'Authorization': 'Bearer ' + token_obj.access_token,
            'Content-Type': 'application/json; UTF-8',
        }
        request_url = 'https://fcm.googleapis.com/v1/projects/{}/messages:send'.format('kredi-f4f77')
        message = {
            "message": {
                "token": token,
                "notification": {
                    "title": title,
                    "body": body
                },
                "data": {
                    "story_id": "story_12345"
                }
            }
        }
        response = requests.post(request_url, data=json.dumps(message), timeout=60, headers=headers)
        return response

    def send_to_token(self, token, title, body, data={}):

        response = ''
        if token:
            try:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=title,
                        body=body,
                    ),
                    token=token,
                    data=data,
                )

                response = messaging.send(message, app=self.APP)
                # write_log('firebase_send_to_token', response)
                third_logger.info('firebase_send_to_token: {}'.format(response))
            except Exception as e:
                # write_log('firebase_send_to_token_error', traceback.format_exc())
                third_logger.error('firebase_send_to_token_error: {}, {}'.format(traceback.format_exc(), e))
                response = e
        return response

    def send_to_all(self, title, body, topic='/topics/all'):
        # third_logger.info('TOKEN={}'.format(self.APP.get_access_token()))
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                topic=topic
            )
            response = messaging.send(message, app=self.APP)
            third_logger.info('firebase_send_to_all: {}'.format(response))
            # write_log('firebase_send_to_all', response)
        except Exception as e:
            # write_log('firebase_send_to_all_error', traceback.format_exc())
            third_logger.error('firebase_send_to_all_error: {}'.format(traceback.format_exc()))

    def subscribe(self, token, topic):
        try:
            response = messaging.subscribe_to_topic([token], topic, app=self.APP)
            third_logger.info('firebase_subscribe: {}'.format(response))
        except Exception as e:
            third_logger.error('firebase_subscribe_error: {}'.format(traceback.format_exc()))

        return response
