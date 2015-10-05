# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.db.models import permalink


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    html_content = models.TextField(verbose_name='html格式内容')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    slug = models.SlugField(unique=True, max_length=100)

    def __unicode__(self):
        return self.title

    class Media(object):
        verbose_name = '文章'
        verbose_name_plural = '文章'

    @permalink
    def get_absolute_url(self):
        return ('blog:articleview', None, {'slug': self.slug, })
