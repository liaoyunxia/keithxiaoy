import json
import logging
import random
import traceback

import googlemaps
from django.conf import settings
from redis import StrictRedis

logger = logging.getLogger('error')

keys = [
    'AIzaSyDZV3J0temlE8sGkN19LqVOyXELvnEelW0',
    # 'AIzaSyAhY-v7TqtWsWw_uzQZ35pDMAieFFOqoWw',
    'AIzaSyAg3qRRAEwy7mzQjli-WQorieZbcaNJljE'
]


class Google_Map():
    def __init__(self, key=None):
        if key:
            self.gmaps = googlemaps.Client(key=key, timeout=60)
            # self.add_map_count(keys.index(key))
        else:
            top = self.get_map_top()
            if not top:
                top = random.randint(0, len(keys) - 1)
            self.gmaps = googlemaps.Client(key=keys[int(top)], timeout=60)
            self.add_map_count(int(top))

    def get_location(self, address):
        try:
            # Geocoding an address
            geocode_result = self.gmaps.geocode(address)
            data = ''
            latitude = ''
            longitude = ''
            is_success = False
            if len(geocode_result) > 0:
                data = json.dumps(geocode_result)
                latitude = geocode_result[0]['geometry']['location']['lat']
                longitude = geocode_result[0]['geometry']['location']['lng']
                is_success = True
        except Exception as e:
            logger.error('google_map_get_location_error: {}'.format(traceback.format_exc()))
            data = ''
            latitude = ''
            longitude = ''
            is_success = False
        return data, latitude, longitude, is_success

    def get_address(self, lat, lng, result_type):
        try:
            # Geocoding an address
            reverse_geocode_result = self.gmaps.reverse_geocode((lat, lng), result_type=result_type)
            logger.info('google_map_get_address: {}'.format(reverse_geocode_result))
        except Exception as e:
            logger.error('google_map_get_address_error: {}'.format(traceback.format_exc()))
            reverse_geocode_result = None
            raise e
        return reverse_geocode_result

    def get_map_top(self):
        redis = StrictRedis(settings.KV_REDIS, password=settings.KV_REDIS_PASSWORD)
        uids = redis.zrange('map', 0, 1)
        if len(uids) > 0:
            return uids[0]
        return None

    def get_map_list(self):
        redis = StrictRedis(settings.KV_REDIS, password=settings.KV_REDIS_PASSWORD)
        uids = redis.zrange('map', 0, -1)
        return uids

    def clear_map_count(self):
        for i in range(0, len(keys)):
            uids = self.get_map_list()
            for uid in uids:
                self.insert_map_count(uid)

    def insert_map_count(self, index):
        redis = StrictRedis(settings.KV_REDIS, password=settings.KV_REDIS_PASSWORD)
        redis.zadd('map', {index: 0})

    def add_map_count(self, index):
        redis = StrictRedis(settings.KV_REDIS, password=settings.KV_REDIS_PASSWORD)
        redis.zincrby('map', 1, index)
