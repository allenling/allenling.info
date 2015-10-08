# coding=utf-8
from __future__ import unicode_literals
import os
import subprocess
import logging
from docutils.core import publish_parts

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'allenling.settings')
import django
django.setup()

from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify

from blog.models import Article

name = __name__.split('.')[0]

logger = logging.getLogger(name)


def create_article():
    articles = [a for a in os.listdir(os.environ['GIT_REPO_PATH']) if a.endswith('.rst')]
    articles_list = []
    for article in articles:
        with open(os.path.join(os.environ['GIT_REPO_PATH'], article), 'r') as f:
            tmp_dict = dict(title=article, slug=slugify(article), html_content=mark_safe(publish_parts(f, writer='html')['html_body']).strip())
            articles_list.append(Article(**tmp_dict))
    Article.objects.bulk_create(articles_list)


def update_article(articles):
    if not articles:
        return
    for article in articles:
        title = article.split('b/')[1]
        with open(os.path.join(os.environ['GIT_REPO_PATH'], article), 'r') as f:
            article, created = Article.objects.get_or_create(title=title, defaults={'html_content': mark_safe(publish_parts(f, writer='html')['html_body']).strip(),
                                                                                    'slug': slugify(title)})
            if not created:
                article.html_content = publish_parts(f, writer='html')['html_body']
                article.slug = slugify(title)
                article.save()


def pull_articles():
    if os.path.isdir(os.environ['GIT_REPO_PATH']):
        subprocess.call(['git', 'clone', os.environ['GIT_REPO_LINK']])
        create_article()
        break
    os.chdir(os.environ['GIT_REPO_PATH'])
    subprocess.call(['git', 'fetch'])
    x = subprocess.check_output(["git", "diff", "master", "origin/master"])
    articles = [i for i in x.splitlines() if 'diff --git ' in i]
    subprocess.call(['git', 'pull'])
    update_article(articles)

if __name__ == '__main__':
    pull_articles()
