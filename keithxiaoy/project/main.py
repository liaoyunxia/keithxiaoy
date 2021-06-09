import logging
import os
import sys

from aiohttp import web
from aiohttp_wsgi import WSGIHandler

from jk_p2p_app.wsgi import application

logger = logging.getLogger(__name__)

# append grpc client to sys.path
client_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clients')
logger.info('client_path: %s', client_path)
sys.path.append(client_path)
for dirname in next(os.walk(client_path))[1]:
    sys.path.append(os.path.join(client_path, dirname))
logger.info('Django main append gRPC clients to sys path successfully')

# Set `inbuf_overflow` up to 128K (default value is 512K)
# try to prevent SpooledTemporaryFile I/O close Exception
wsgi_handler = WSGIHandler(application, inbuf_overflow=1024 * 128)

app = web.Application()
app.router.add_route('*', '/{path_info:.*}', wsgi_handler)
