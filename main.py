import logging
import os
import sys

from aiohttp import web
from aiohttp_wsgi import WSGIHandler

from jk_p2p_app.wsgi import application

logger = logging.getLogger(__name__)

# Set `inbuf_overflow` up to 128K (default value is 512K)
# try to prevent SpooledTemporaryFile I/O close Exception
wsgi_handler = WSGIHandler(application, inbuf_overflow=1024 * 128)

app = web.Application()
app.router.add_route('*', '/{path_info:.*}', wsgi_handler)
