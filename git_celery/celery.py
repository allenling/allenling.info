# coding=utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
import os
from celery import Celery
# 显式setup
try:
    import django
    django.setup()
except AttributeError:
    pass

name = __name__.split('.')[0]
celery = Celery(__name__,
                broker=os.environ.get("%s.broker" % name, "amqp://guest:guest@localhost:5672//"),  # should be replaced by environ
                )

celery.config_from_object('%s.celeryconfig' % name)
