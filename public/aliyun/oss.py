from __future__ import print_function
import datetime
import random
import time

from urllib.parse import unquote

import oss2
import requests
import json

from django.conf import settings

from ..utils.func_ext import create_filename


class AliyunOss:
    def __init__(self):
        endpoint = "http://{}".format(settings.CLOUD_SS_BASE_DOMAIN_NAME)
        public_endpoint = endpoint
        auth = oss2.Auth(settings.CLOUD_SS_ID, settings.CLOUD_SS_SECRET)
        self.bucket = oss2.Bucket(auth, public_endpoint, settings.BUCKET_MEDIA)

    def upload_network_file(self, filename, file_url):
        try:
            self.bucket.put_object(filename, requests.get(file_url, timeout=60))
        except:
            filename = ''
        return filename

    def copy_file(self, filename, new_filename):
        try:
            self.bucket.copy_object(settings.BUCKET_MEDIA, unquote(filename), new_filename)
        except:
            new_filename = ''
        return new_filename

    def upload_json(self, filename, data):
        try:
            self.bucket.put_object(filename, data)
        except:
            filename = ''
        return filename

    def download_file(self, filename):
        object_stream = self.bucket.get_object(filename)
        data = object_stream.read()
        data = str(data, 'utf-8')
        res = json.loads(data)
        return res
