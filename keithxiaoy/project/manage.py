# -*-coding:utf-8-*-
import logging
import os
import sys

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jk_p2p_app.settings')

    # append grpc client to sys.path
    client_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clients')
    logger.info('client_path: %s', client_path)
    sys.path.append(client_path)
    for dirname in next(os.walk(client_path))[1]:
        sys.path.append(os.path.join(client_path, dirname))
    logger.info('Django manage append gRPC clients to sys path successfully')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
