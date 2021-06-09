{{ project_name }}
==================

Quickstart
==========

install 
```bash
cd ~/workspace
django-admin.py startproject --template=django_layout {{ project_name }}
cd ~/workspace/{{ project_name }}
fab local_install
fab local_compilemessages
```
run
```bash
cd ~/workspace/{{ project_name }}
fab local_runserver
```
if case 500 error
chech cache server is setting

Introduction
============
Tips
----

worker count advic= 1 + 2 * cpu count

Django
------

[Design Document]: https://github.com/nyssance/{{ project_name }}/blob/master/Docs/test.md

tool
- [Fabric](https://www.fabfile.org)
- [Colorama]https://github.com/tartley/colorama)

frame
- [Railgun S](https://github.com/nyssance/railguns)

project
- [django-currentuser](https://github.com/PaesslerAG/django-currentuser)
- [Django Suit](http://djangosuit.com)
- [django-import-export](https://django-import-export.readthedocs.io)
- [DRF-extensions](https://chibisov.github.io/drf-extensions/docs/)
- [Haystack](https://github.com/django-haystack/django-haystack)

wechat
- [wechatpy](https://github.com/jxtech/wechatpy/)
- [REST Framework XML](https://jpadilla.github.io/django-rest-framework-xml/)

fontend
- [QR Code Generator](https://github.com/kazuhikoarase/qrcode-generator/tree/master/js)
- [Swiper](https://www.swiper.com.cn)


debug
- [django-cors-headers](https://github.com/ottoyiu/django-cors-headers)
- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io)
- [Django Haystack Panel](https://github.com/streeter/django-haystack-panel)

language
- [Rosetta](https://django-rosetta.readthedocs.io)
- [Transifex](https://docs.transifex.com)

deploy
- [Ubuntu](https://www.ubuntu.com)
- [NGINX](https://www.nginx.com)
- [Supervisor](http://supervisord.org)
- [Gunicorn](https://gunicorn.org)
- [aiohttp](https://aiohttp.readthedocs.io)
- [aiohttp-wsgi](https://aiohttp-wsgi.readthedocs.io)
- [uvloop](https://uvloop.readthedocs.io)

backend
self.get_model().objects.filter(user_id=self.kwargs[self.lookup_field], type__gte=1000, is_active=True)


# Code Formatter

1. Install `yapf` in your native environment `python3 -m pip install yapf`
2. Search and install `yapf` PyCharm plugin
3. Turn on the `Format on Save` option in `yapf` settings

More about [auto formatter in Python](https://www.kevinpeters.net/auto-formatters-for-python)

Tips: Auto format is according to `.editorconfig` and `setup.cfg`

### dev requirements

```bash
pip install -U -r requirements/dev.txt -i https://pypi.douban.com/simple
```
