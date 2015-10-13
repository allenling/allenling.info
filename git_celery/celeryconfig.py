# coding=utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from kombu.entity import Exchange, Queue
from celery.schedules import crontab
name = __name__.split('.')[0]
CELERYD_PREFETCH_MULTIPLIER = 1

# Message Routing
CELERY_QUEUES = (Queue('SYNC_ARTICLE', Exchange('SYNC_ARTICLE', type='direct'), routing_key='SYNC_ARTICLE'),
                 )
CELERY_ROUTES = {'%s.tasks.SYNC_ARTICLE' % name: {'queue': 'SYNC_ARTICLE'},
                 }

# Broker Settings
CELERY_ACCEPT_CONTENT = ('json',)
BROKER_HEARTBEAT = 10
BROKER_HEARTBEAT_CHECKRATE = 1
BROKER_POOL_LIMIT = 0
CELERY_IGNORE_RESULT = False
CELERY_MAX_CACHED_RESULTS = 3000
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_TASK_PUBLISH_RETRY_POLICY = {
    'max_retries': 4,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2,
}

# Task execution settings
CELERY_TRACK_STARTED = False
CELERY_TASK_SERIALIZER = 'json'
CELERY_DEFAULT_RATE_LIMIT = 0
CELERY_DISABLE_RATE_LIMITS = False
CELERY_ACKS_LATE = True

# worker settings
CELERY_IMPORTS = ('%s.tasks' % name,)
CELERYD_WORKER_LOST_WAIT = 10.0
CELERYD_TASK_TIME_LIMIT = 1200.0
CELERYD_TASK_SOFT_TIME_LIMIT = 0  # not supported on windows
CELERYD_POOL_RESTARTS = True
CELERYD_MAX_TASKS_PER_CHILD = 1000
# CELERYD_HIJACK_ROOT_LOGGER = False
# CELERY_ALWAYS_EAGER = True

CELERYBEAT_SCHEDULE = {'sync-every-day': {'task': '%s.tasks.sync_article' % name,
                                                  'schedule': crontab(hour=23, minute=50),
                                          },
                       }
