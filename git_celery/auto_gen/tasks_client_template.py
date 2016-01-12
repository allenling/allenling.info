# coding=utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from .celery import celery


@celery.task
def sync_article():
    return
