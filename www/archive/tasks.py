from __future__ import absolute_import

from fb_archive import celery_app as app
from celery import shared_task

from .fb_request import FBRequest

import logging
from .models import User, Group, Post, Comment, Media, Attachment

__author__ = "Donghyun Seo"
__copyright__ = "Copyright ⓒ 2015, All rights reserved."
__email__ = "egaoneko@naver.com"

logger = logging.getLogger(__name__)
fb_request = FBRequest()


@shared_task
def store_user(user_id, user_name, group):
    """
    This method stores a user.

    :param user_id: user id
    :param user_name:  user name
    :return: user model
    """
    user = User.objects.filter(id=user_id)
    if not user:
        # save user
        user = User(id=user_id, name=user_name)
        user.picture = fb_request.user_picture(user_id)
        user.save()
        logger.info('Saved user: %s', user.id)
    else:
        user = user[0]

    user.groups.add(group)

    return user


@shared_task
def store_attachment(attachment_data, post=None, comment=None):
    """
    This method stores a attachment. You must put one of post or comment.

    :param attachment_data: attachment data(dictionary)
    :param post: post model for foreign key
    :param comment: comment model for foreign key
    :return:
    """
    attachment = Attachment()
    if post is not None:
        attachment.post = post
    if comment is not None:
        attachment.comment = comment
    if 'url' in attachment_data:
        attachment.url = attachment_data.get('url')
    if 'title' in attachment_data:
        attachment.title = attachment_data.get('title')
    if 'description' in attachment_data:
        attachment.description = attachment_data.get('description')
    if 'type' in attachment_data:
        attachment.type = attachment_data.get('type')
    if 'media' in attachment_data:
        media = Media(height=attachment_data.get('media').get('image').get('height'),
                      width=attachment_data.get('media').get('image').get('width'),
                      src=attachment_data.get('media').get('image').get('src'))
        media.save()
        logger.info('Saved media: %s', media.id)
        attachment.media = media
    attachment.save()
    logger.info('Saved attachment: %s', attachment.id)

    # store sub attachments
    if 'subattachments' in attachment_data:
        for subattachment_data in attachment_data.get('subattachments').get('data'):
            if post is not None:
                attachment.post = post
                store_attachment(attachment_data=subattachment_data, post=post)

            if comment is not None:
                attachment.comment = comment
                store_attachment(attachment_data=subattachment_data, comment=comment)


@shared_task
def store_comment(comment_data, post, group, parent=None):
    """
    This method stores a comment. If you want to store reply, put parent.

    :param comment_data: comment data(dictionary)
    :param post: post model for foreign key
    :param group: comment's group
    :param parent: comment model for parent
    :return:
    """
    comment_id = comment_data.get('id')
    if not Comment.objects.filter(id=comment_id).exists():
        comment = Comment(id=comment_id)
        comment.post = post

        # save user
        comment_from = comment_data.get('from')
        comment.user = store_user(comment_from.get('id'), comment_from.get('name'), group)

        comment.created_time = comment_data.get('created_time')
        comment.like_count = comment_data.get('like_count')
        comment.group = group

        if 'message' in comment_data:
            comment.message = comment_data.get('message')

        if parent is not None:
            comment.parent = parent

        comment.save()
        group.comment_count += 1
        group.save()
        logger.info('Saved comment: %s', comment.id)

        if 'attachment' in comment_data:
            store_attachment(attachment_data=comment_data.get('attachment'), comment=comment)
    else:
        comment = Comment.objects.filter(id=comment_id)[0]
        comment.like_count = comment_data.get('like_count')

        if 'message' in comment_data:
            comment.message = comment_data.get('message')

        comment.save()
        logger.info('Updated comment: %s', comment.id)

    # store reply comments
    if 'comments' in comment_data:
        for reply_comment_data in comment_data.get('comments').get('data'):
            store_comment(comment_data=reply_comment_data, post=post, group=group, parent=parent)


@shared_task
def store_feed(feed_data, group):
    """
    This method stores a feed.

    :param feed_data: feed data(dictionary)
    :param group: post's group
    :return:
    """
    # save post from feeds
    post_id = feed_data.get('id')
    if not Post.objects.filter(id=post_id).exists():
        post = Post(id=post_id)

        # save user
        post_from = feed_data.get('from')
        post.user = store_user(post_from.get('id'), post_from.get('name'), group)

        post.message = feed_data.get('message')
        post.created_time = feed_data.get('created_time')
        post.updated_time = feed_data.get('updated_time')
        post.picture = feed_data.get('picture')
        post_comments = feed_data.get('comments')
        post.comment_count = post_comments.get('summary').get('total_count')
        post.like_count = feed_data.get('likes').get('summary').get('total_count')
        post.group = group

        if 'shares' in feed_data:
            post.share_count = feed_data.get('shares').get('count')
        else:
            post.share_count = 0

        post.save()
        group.post_count += 1
        group.save()
        logger.info('Saved post: %s', post.id)

        # save attachments
        post_attachments = feed_data.get('attachments')
        if post_attachments:
            for attachment_data in post_attachments.get('data'):
                store_attachment(attachment_data=attachment_data, post=post)
    else:
        post = Post.objects.filter(id=post_id)[0]

        if post.is_updated(feed_data.get('updated_time')):

            post.message = feed_data.get('message')
            post.updated_time = feed_data.get('updated_time')
            post.picture = feed_data.get('picture')
            post_comments = feed_data.get('comments')
            post.comment_count = post_comments.get('summary').get('total_count')
            post.like_count = feed_data.get('likes').get('summary').get('total_count')

            if 'shares' in feed_data:
                post.share_count = feed_data.get('shares').get('count')
            else:
                post.share_count = 0

            post.save()
            logger.info('Updated post: %s', post.id)
        else:
            return False

    # get all comments by using graph api and loop
    post_comments_data = post_comments.get('data')
    if 'paging' in post_comments:
        comment_paging = post_comments.get('paging')
        if 'next' in comment_paging:
            comments_query = fb_request.get_comment_next_query(comment_paging.get('next'))
            while comments_query is not None:
                comments_query = fb_request.comment(comments_query, post_comments_data)

    # save comments
    for comment_data in post_comments_data:
        store_comment(comment_data=comment_data, post=post, group=group)

    return True


@shared_task
def store_group_feed(group_id, query, is_whole=False):
    """
    This method is storing group's feeds by using facebook group api.
    If you want to get whole data, put that 'is_whole' is true.

    :param group_id: param group_id: group id for getting feeds
    :param query: query for facebook graph api
    :param is_whole: whole or parts
    :return:
    """
    logger.info('Saving %s feed', group_id)
    group = Group.objects.filter(id=group_id)[0]

    feeds = []

    if is_whole:
        while query is not None:
            query = fb_request.feed(group, query, feeds)
    else:
        fb_request.feed(group, query, feeds)

    for feed in feeds:
        store_feed(feed, group)

    group.is_stored = True
    group.save()


@shared_task
def update_group_feed(group_id, query, is_whole=False):
    """
    This method is updating group's feeds by using facebook group api.
    If you want to get whole data, put that 'is_whole' is true.

    :param group_id: param group_id: group id for getting feeds
    :param query: query for facebook graph api
    :param is_whole: whole or parts
    :return: success?
    """
    logger.info('Updating %s feed', group_id)
    updated_time = fb_request.group(group_id).get('updated_time')
    group = Group.objects.filter(id=group_id)[0]

    if not group.is_updated(updated_time):
        return False

    group.updated_time = updated_time
    group.save()
    logger.info('Update group updated_time: %s', group.id)

    feeds = []

    if is_whole:
        while query is not None:
            query = fb_request.feed(group, query, feeds)
            for feed in feeds:
                if not store_feed(feed, group):
                    return True
            feeds = []
    else:
        fb_request.feed(group, query, feeds)
        for feed in feeds:
            if not store_feed(feed, group):
                return True

    return True


@shared_task
def update_groups_feed(query, is_whole=False):
    """
    This method is updating group's feeds by using facebook group api for celery schedule.
    If you want to get whole data, put that 'is_whole' is true.

    :param query: query for facebook graph api
    :param is_whole: whole or parts
    :return:
    """
    groups = Group.objects.values('id')

    for group in groups:
        update_group_feed(group.get('id'), query, is_whole)
