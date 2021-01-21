from django.apps import AppConfig
from railguns.django.utils.apps import get_name


class Config(AppConfig):
    name = get_name(__file__)
