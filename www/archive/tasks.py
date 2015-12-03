from __future__ import absolute_import
import logging
from time import sleep

from django.utils import timezone
from facebook import GraphAPIError
from celery import shared_task
from archive.fb.fb_request import FBRequest
from .models import User, Group, Post, Comment, Media, Attachment, Blacklist, DeletedPost, DeletedComment

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

        if 'comments' in comment_data:
            comment.comment_count = comment_data.get('comments').get('summary').get('total_count')

        if 'message' in comment_data:
            comment.message = comment_data.get('message')

        if parent is not None:
            comment.parent = parent

        comment.save()
        logger.info('Saved comment: %s', comment.id)

        if 'attachment' in comment_data:
            store_attachment(attachment_data=comment_data.get('attachment'), comment=comment)
    else:
        comment = Comment.objects.filter(id=comment_id)[0]
        comment.like_count = comment_data.get('like_count')

        if 'comments' in comment_data:
            comment.comment_count = comment_data.get('comments').get('summary').get('total_count')

        if 'message' in comment_data:
            comment.message = comment_data.get('message')

        comment.save()
        logger.info('Updated comment: %s', comment.id)

    # store reply comments
    if 'comments' in comment_data:
        for reply_comment_data in comment_data.get('comments').get('data'):
            comment = Comment.objects.filter(id=comment_id)[0]
            store_comment(comment_data=reply_comment_data, post=post, group=group, parent=comment)


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
def store_group(group_data):
    """
    This method stores a group.

    :param group_data: feed data(dictionary)
    :return:
    """
    group_id = group_data.get('id')
    if not Group.objects.filter(id=group_id).exists():
        group = Group()
        group.id = group_data.get('id')
        group.name = group_data.get('name')
        group.description = group_data.get('description')
        group.updated_time = group_data.get('updated_time')
        group.privacy = group_data.get('privacy')
        group.save()
        group.owner = store_user(group_data.get('owner').get('id'), group_data.get('owner').get('name'), group)
        group.save()
        logger.info('Saved group: %s', group)
    else:
        group = Group.objects.filter(id=group_id)[0]
        group.name = group_data.get('name')
        group.description = group_data.get('description')
        group.updated_time = group_data.get('updated_time')
        group.privacy = group_data.get('privacy')
        group.owner = store_user(group_data.get('owner').get('id'), group_data.get('owner').get('name'), group)
        group.save()
        logger.info('Update group updated_time: %s', group.id)
    return group


@shared_task
def check_cp_cnt_group(group):
    """
    Check comment and post count in group.

    :param group: group
    :return:
    """
    group.post_count = group.posts.count()
    group.comment_count = group.comments.count()
    group.save()


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
    logger.info('=== Start saving %s feed ===', group_id)
    start_time = timezone.datetime.now().replace(microsecond=0)
    logger.info('Start time : %s', start_time)

    group = Group.objects.filter(id=group_id)[0]

    if group.privacy == "CLOSED":
        logger.info('=== Fail to save %s feed (Group is closed) ===', group_id)
        return False

    feeds = []

    while query is not None:
        query = fb_request.feed(group, query, feeds)
        sleep(1)
        if not is_whole:
            break

    for feed in feeds:
        try:
            store_feed(feed, group)
        except Exception as e:
            logger.info('Fail to store by exception : %s', e)
            try:
                store_feed(feed, group)
            except Exception as e:
                logger.info('Fail to store again by exception : %s', e)

    group.is_stored = True
    group.save()
    check_cp_cnt_group(group)

    end_time = timezone.datetime.now().replace(microsecond=0)
    logger.info('End time : %s', end_time)
    logger.info('Time difference : %s', end_time - start_time)
    logger.info('=== End saving %s feed ===', group_id)


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
    logger.info('=== Start updating %s feed ===', group_id)
    start_time = timezone.datetime.now().replace(microsecond=0)
    logger.info('Start time : %s', start_time)

    try:
        group_data = fb_request.group(group_id)
    except Exception as e:
        logger.info('Fail to get group data by exception : %s', e)
        try:
            group_data = fb_request.group(group_id)
        except Exception as e:
            logger.info('Fail to get group data again by exception : %s', e)
            return False

    updated_time = group_data.get('updated_time')
    group = Group.objects.filter(id=group_id)[0]

    if not group.is_updated(updated_time):
        logger.info('=== Fail to update %s feed (Already updated) ===', group_id)
        return False

    if group.privacy == "CLOSED":
        logger.info('=== Fail to update %s feed (Group is closed) ===', group_id)
        return False

    store_group(group_data)

    feeds = []

    while query is not None:
        query = fb_request.feed(group, query, feeds)
        for feed in feeds:
            try:
                res = store_feed(feed, group)
            except Exception as e:
                logger.info('Fail to update by exception : %s', e)
                try:
                    res = store_feed(feed, group)
                except Exception as e:
                    logger.info('Fail to update again by exception : %s', e)
            if not res:
                check_cp_cnt_group(group)
                return True
        feeds = []
        if not is_whole:
            break

    check_cp_cnt_group(group)

    end_time = timezone.datetime.now().replace(microsecond=0)
    logger.info('End time : %s', end_time)
    logger.info('Time difference : %s', end_time - start_time)
    logger.info('=== End updating %s feed ===', group_id)
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
    logger.info('=== Start updating groups ===')
    start_time = timezone.datetime.now().replace(microsecond=0)
    logger.info('Start time : %s', start_time)
    groups = Group.objects.values('id')

    for group in groups:
        update_group_feed(group.get('id'), query, is_whole)

    end_time = timezone.datetime.now().replace(microsecond=0)
    logger.info('End time : %s', end_time)
    logger.info('Time difference : %s', end_time - start_time)
    logger.info('=== End updating groups ===')


def delete_group_content(object_id, model):
    """
    Delete group content

    :param object_id: object_id
    :param model: model (post or comment)
    :return:
    """
    # Find object in our site
    try:
        if model == 'post':
            content = Post.objects.get(pk=object_id)
        else:
            content = Comment.objects.get(pk=object_id)
    except (Post.DoesNotExist, Comment.DoesNotExist):
        return True, "Successfully deleted, but '" + object_id + "' does not exist in our site."

    # Delete object in our site with related object
    if isinstance(content, Post):
        deleted_post = DeletedPost.create(content)
        deleted_post.save()
        comments = Comment.objects.filter(post=content)

        if comments:
            for comment in comments:
                deleted_comment = DeletedComment.create(comment)
                deleted_comment.save()

            for comment in comments:
                comment.delete()
    else:
        deleted_comment = DeletedComment.create(content)
        deleted_comment.save()

        child_comments = Comment.objects.filter(parent=content)
        if child_comments:
            for child_comment in child_comments:
                deleted_comment = DeletedComment.create(child_comment)
                deleted_comment.save()

            for child_comment in child_comments:
                child_comment.delete()

    content.delete()

    # Add blacklist count
    try:
        bl = Blacklist.objects.get(group=content.group, user=content.user)
    except Blacklist.DoesNotExist:
        bl = Blacklist(group=content.group, user=content.user)

    bl.count += 1
    bl.save()

    return True, None


def delete_group_content_by_fb(object_id, model, _fb_request=fb_request):
    """
    Delete group content by fb request

    :param _fb_request: fb request
    :param object_id: object_id
    :param model: model (post or comment)
    :return:
    """
    # Delete object in facebook
    try:
        _fb_request.delete_object(object_id)
    except GraphAPIError as e:
        return False, e.__str__()

    return delete_group_content(object_id, model)
