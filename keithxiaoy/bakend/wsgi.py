import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jk_p2p_app.settings')

application = get_wsgi_application()
