# coding=utf-8
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

from .models import Article


def index(request):
    context = {'articles': Article.objects.all().order_by('update_time')
               }
    return render(request, 'blog/index.html', context)


def ArticleViews(request, slug):
    context = dict(article=get_object_or_404(Article, slug=slug))
    return render(request, 'blog/article.html', context)
