from __future__ import absolute_import, unicode_literals

import logging
import os
import sys

from celery import Celery
# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab
from celery.signals import task_failure
from django.conf import settings
from kombu import Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jk_p2p_app.settings')

logger = logging.getLogger('task')

# append grpc client to sys.path
client_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'clients',
)
logger.info('client_path: %s', client_path)
sys.path.append(client_path)
for dirname in next(os.walk(client_path))[1]:
    sys.path.append(os.path.join(client_path, dirname))
logger.info('Celery append gRPC clients to sys path successfully')

app = Celery('jk_p2p_app')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

redis_url = f'redis://:{settings.KV_REDIS_PASSWORD}@{settings.KV_REDIS}:6379/2'

app.conf.ONCE = {
    'backend': 'celery_once.backends.Redis',
    'settings': {
        'url': redis_url,
        'default_timeout': 60 * 60,
    }
}
app.conf.timezone = 'Asia/Jakarta'
app.conf.beat_schedule = {
    'callback-loan-8-clock': {
        'task': 'jk_p2p_app.apps.api.tasks.callback_apply_loan',
        'schedule': crontab(minute='*/3') if settings.SPEED_UP_CELERY_BEAT else crontab(hour=8, minute=0),
        'options': {
            'queue': 'default',
            'routing_key': 'tasks.callback_apply_loan'
        }
    },
    'reminder-repay-8-0-clock': {
        'task': 'jk_p2p_app.apps.api.tasks.collection_pre_n',
        'schedule': crontab(hour=8, minute=0),
        'options': {
            'queue': 'default',
            'routing_key': 'tasks.collection_pre_n'
        }
    },
    'callback-airudder-9-0-clock': {
        'task': 'jk_p2p_app.apps.api.tasks.callback_ai_warning',
        'schedule': crontab(hour=9, minute=0),
        'options': {
            'queue': 'default',
            'routing_key': 'tasks.callback_ai_warning'
        }
    },
    'callback-userreloan-9-0-clock': {
        'task': 'jk_p2p_app.apps.api.tasks.callback_apply_loan_ivr',
        'schedule': crontab(hour=9, minute=0),
        'args': (1, 3, 2),
        'options': {
            'queue': 'default',
            'routing_key': 'tasks.callback_apply_loan_ivr'
        }
    },
    'callback-pass-credited-8-0-clock': {
        'task': 'jk_p2p_app.apps.api.tasks.callback_apply_loan_ivr',
        'schedule': crontab(hour=13, minute=55),
        'args': (1, 3, 1),
        'options': {
            'queue': 'default',
            'routing_key': 'tasks.callback_apply_loan_ivr'
        }
    },
    'callback-money-clear-11-clock': {
        'task': 'jk_p2p_app.apps.api.tasks.callback_invite_user',
        'schedule': crontab(hour=11, minute=0),
        'options': {
            'queue': 'default',
            'routing_key': 'tasks.callback_invite_user'
        }
    },
    'callback-october-activity-8-0-clock': {
        'task': 'jk_p2p_app.apps.api.tasks.october_activity_notice',
        'schedule': crontab(hour=8, minute=0),
        'options': {
            'queue': 'default',
            'routing_key': 'tasks.october_activity_notice'
        }
    },
    'december-activity-notice-9-0-click': {
        'task': 'jk_p2p_app.apps.api.tasks.december_activity_notice',
        'schedule': crontab(hour=9, minute=0),
    },
    'december-signup-notice-10-0-click': {
        'task': 'jk_p2p_app.apps.api.tasks.invite_december_signup_activities',
        'schedule': crontab(hour=10, minute=0),
    },
    # cur_n_push
    'notice-collection-n-every-day': {
        'task': 'jk_p2p_app.apps.api.tasks.collection_n',
        'schedule': 100.0 if settings.SPEED_UP_CELERY_BEAT else crontab(hour=8, minute=0),
        'options': {
            'queue': 'default',
            'routing_key': 'tasks.collection_n'
        }
    },
    # cur_n_sms
    'sms-collection-n-every-day': {
        'task': 'jk_p2p_app.apps.api.tasks.collection_n_sms',
        'schedule': 100.0 if settings.SPEED_UP_CELERY_BEAT else crontab(hour=8, minute=0),
        'options': {
            'queue': 'default',
            'routing_key': 'tasks.collection_n_sms'
        }
    },
    # overdue payday collection
    'payday-collection-every-day': {
        'task': 'jk_p2p_app.apps.api.tasks.payday_collection',
        'schedule': 150.0 if settings.SPEED_UP_CELERY_BEAT else crontab(hour=8, minute=0),
    },
    # overdue installment collection
    'installment-collection-every-day': {
        'task': 'jk_p2p_app.apps.api.tasks.installment_collection',
        'schedule': 100.0 if settings.SPEED_UP_CELERY_BEAT else crontab(hour=8, minute=0),
    },
    # end activity
    'disable-activity': {
        'task': 'jk_p2p_app.apps.api.tasks.disable_activity',
        'schedule': 100.0 if settings.SPEED_UP_CELERY_BEAT else crontab(hour=0, minute=0),
    },
}

app.conf.task_default_queue = 'default'
app.conf.task_queues = (
    Queue('default', routing_key='task.#'),
    Queue('message', routing_key='message.#'),
    Queue('sync', routing_key='sync.#'),
)
app.conf.task_default_exchange = 'tasks'
app.conf.task_default_exchange_type = 'topic'
app.conf.task_default_routing_key = 'tasks.default'
app.conf.task_routes = {
    # message queue
    'jk_p2p_app.apps.api.tasks.recall_installed_users': {
        'queue': 'message',
        'routing_key': 'message.recall_installed_users',
    },
    'jk_p2p_app.apps.api.tasks.recall_credit_not_started': {
        'queue': 'message',
        'routing_key': 'message.recall_credit_not_started',
    },
    'jk_p2p_app.apps.api.tasks.recall_credit_not_complete': {
        'queue': 'message',
        'routing_key': 'message.recall_credit_not_complete',
    },
    'jk_p2p_app.apps.api.tasks.recall_credit_rollback': {
        'queue': 'message',
        'routing_key': 'message.recall_credit_rollback',
    },
    'jk_p2p_app.apps.api.tasks.recall_credited_users': {
        'queue': 'message',
        'routing_key': 'message.recall_credited_users',
    },
    'jk_p2p_app.apps.api.tasks.recall_settled_users': {
        'queue': 'message',
        'routing_key': 'message.recall_settled_users',
    },
    'jk_p2p_app.apps.api.tasks.recall_bank_vr': {
        'queue': 'message',
        'routing_key': 'message.recall_bank_vr',
    },
    # sync queue
    'jk_p2p_app.apps.accounts.tasks.distribute_user': {
        'queue': 'sync',
        'routing_key': 'sync.distribute_user',
    },
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks([
    'jk_p2p_app.apps.accounts.tasks',
    'jk_p2p_app.apps.api.tasks',
    'jk_p2p_app.apps.orders.tasks',
    'jk_p2p_app.apps.notification.tasks',
    'jk_p2p_app.apps.marketing.tasks',
])


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, args=None, traceback=None, **kwargs):
    import logging
    # noinspection PyShadowingNames
    logger = logging.getLogger('task')
    logger.error(
        'Celery task failed sender: %s, task_id: %s, exception: %s, traceback: %s, args: %s, kwargs: %s', sender,
        task_id, exception, traceback, args, kwargs
    )
