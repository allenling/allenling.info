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


def update_article(action, title):
    # 删除
    acticle = Article.objects.get(title=title)
    if action == 'D':
        acticle.delete()
        return
    # 修改或者新增, 直接update_or_create
    elif action == 'M' or action == 'A':
        with open(os.path.join(os.environ['GIT_REPO_PATH'], title)) as f:
            Article.objects.update_or_create(title=title, defaults={'html_content': mark_safe(publish_parts(f, writer='html')['html_body']).strip(),
                                                                    'slug': slugify(title)})
    else:
        logger.warning('unkwon git action: %s, article: %s', action, title)


def sync_article():
    if os.path.isdir(os.environ['GIT_REPO_PATH']):
        subprocess.call(['git', 'clone', os.environ['GIT_REPO_LINK']])
        current_header = subprocess.check_output(['git', 'log', "--pretty=format:'%h'", '-n', '1']).replace("'", "")
        logger.info('git clone, and header: %s', current_header)
        create_article()
        break
    os.chdir(os.environ['GIT_REPO_PATH'])
    pull_res = subprocess.check_output(['git', 'pull'])
    # 没有更新
    if pull_res == 'Already up-to-date.\n':
        return
    # 取最后一个commit的hash值
    current_header = subprocess.check_output(['git', 'log', "--pretty=format:'%h'", '-n', '1']).replace("'", "")
    logger.info('git header: %s', current_header)
    # 修改的文件
    log_res = subprocess.check_output(['git', 'diff-tree', '--no-commit-id -r', current_header])
    for f in log_res.splitline():
        action, rst = f.split(' ')[-1].split('\t')
        # 非.rst文件不track
        if not rst.endswith('.rst'):
            continue
        # 获取文章标题
        title = os.path.splitext(rst)[0]
        update_article(action, title)

if __name__ == '__main__':
    sync_article()
    print 'sync article done!'
