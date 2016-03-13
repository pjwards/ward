# The MIT License (MIT)
#
# Copyright (c) 2015 pjwards.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==================================================================================
""" Provides functions for storing facebook data by using celery """

from __future__ import absolute_import
from celery import shared_task
from archive.fb.fb_tasks import *

logger = logging.getLogger(__name__)


@shared_task
def store_group_feed_task(group_id, post_query, comment_query):
    """
    This method is storing group's feeds by using facebook group api.

    :param group_id: param group_id: group id for getting feeds
    :param post_query: post query for facebook graph api
    :param comment_query: comment query for facebook graph api
    :return:
    """
    group = Group.objects.filter(id=group_id)[0]
    store_group_feed(group, post_query)
    check_group_task(group, comment_query)

    group.is_stored = True
    group.save()


@shared_task
def store_group_feed_by_date_task(group_id, post_query, comment_query):
    """
    This method is storing group's feeds for specific date by using facebook group api.

    :param group_id: param group_id: group id for getting feeds
    :param post_query: post query for facebook graph api
    :param comment_query: comment query for facebook graph api
    :return:
    """
    group = Group.objects.filter(id=group_id)[0]
    store_group_feed(group, post_query, True)
    check_group_task(group, comment_query)


@shared_task
def update_group_feed_task(group_id, query):
    """
    This method is updating group's feeds by using facebook group api.

    :param group_id: param group_id: group id for getting feeds
    :param query: query for facebook graph api
    :return: success?
    """
    group = Group.objects.filter(id=group_id)[0]
    update_group_feed(group, query)


@shared_task
def update_groups_feed_task(query):
    """
    This method is updating group's feeds by using facebook group api for celery schedule.

    :param query: query for facebook graph api
    :return:
    """
    logger.info('=== Start updating groups ===')
    groups = Group.objects.values('id')

    for group in groups:
        update_group_feed_task.delay(group.get('id'), query)

    logger.info('=== End updating groups ===')


@shared_task
def check_group_task(group_id, query):
    """
    This method is checking group's comment by using facebook group api.

    :param group_id: param group_id: group id for getting feeds
    :param query: query for facebook graph api
    :return:
    """
    logger.info('=== Start checking %s comments ===', group_id)
    group = Group.objects.filter(id=group_id)[0]
    posts = group.posts.all()

    for post in posts:
        check_group_post_task.delay(post.id, query)

    logger.info('=== End checking %s comments ===', group_id)


@shared_task
def check_group_post_task(post_id, query):
    """
    This method is storing post's comments by using facebook group api.

    :param post_id: param group_id: group id for getting feeds
    :param query: query for facebook graph api
    :return:
    """
    post = Post.objects.filter(id=post_id)[0]
    check_post_comment(post, query)
