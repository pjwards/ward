from __future__ import absolute_import
import logging
from facebook import GraphAPIError
from celery import shared_task
from archive.fb.fb_request import FBRequest
from .models import *

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
    :param group: user group
    :return: user model
    """
    user = FBUser.objects.filter(id=user_id)
    picture = fb_request.user_picture(user_id)
    if not user:
        # save user
        user = FBUser(id=user_id, name=user_name)
        user.picture = picture
        user.save()
        logger.info('Saved user: %s', user.id)
    else:
        user = user[0]
        is_change = False
        if user.name != user_name:
            is_change = True
            user.name = user_name
        elif user.picture != picture:
            is_change = True
            user.picture = picture
        if is_change:
            user.save()
            logger.info('Update user: %s', user.id)

    user.groups.add(group)

    return user


@shared_task
def store_attachment(attachment_data, post_id=None, comment_id=None, use_celery=False):
    """
    This method stores a attachment. You must put one of post or comment.

    :param attachment_data: attachment data(dictionary)
    :param post_id: post id for foreign key
    :param comment_id: comment id for foreign key
    :param use_celery: use celery?
    :return:
    """
    attachment = Attachment()
    if post_id is not None:
        post = Post.objects.filter(id=post_id)[0]
        attachment.post = post
    if comment_id is not None:
        comment = Comment.objects.filter(id=comment_id)[0]
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
            if post_id is not None:
                if use_celery:
                    store_attachment.delay(attachment_data=subattachment_data, post_id=post_id, use_celery=use_celery)
                else:
                    store_attachment(attachment_data=subattachment_data, post_id=post_id, use_celery=use_celery)
            if comment_id is not None:
                if use_celery:
                    store_attachment.delay(attachment_data=subattachment_data, comment_id=comment_id,
                                           use_celery=use_celery)
                else:
                    store_attachment(attachment_data=subattachment_data, comment_id=comment_id, use_celery=use_celery)


@shared_task
def store_comment(comment_data, post_id, group_id, parent_id=None, use_celery=False):
    """
    This method stores a comment. If you want to store reply, put parent.

    :param comment_data: comment data(dictionary)
    :param post_id: post id for foreign key
    :param group_id: comment's group id
    :param parent_id: comment model for parent id
    :param use_celery: use celery?
    :return:
    """
    post = Post.objects.filter(id=post_id)[0]
    group = Group.objects.filter(id=group_id)[0]
    parent = None
    if parent_id is not None:
        parent = Comment.objects.filter(id=parent_id)[0]

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

        # save attachment
        if 'attachment' in comment_data:
            if use_celery:
                store_attachment.delay(attachment_data=comment_data.get('attachment'), comment_id=comment.id,
                                       use_celery=use_celery)
            else:
                store_attachment(attachment_data=comment_data.get('attachment'), comment_id=comment.id,
                                 use_celery=use_celery)
        # save user activity
        UserActivity.add_comment_count(user=comment.user, group=comment.group)
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
            store_comment.delay(comment_data=reply_comment_data, post_id=post.id, group_id=group.id,
                                parent_id=comment.id, use_celery=use_celery)


@shared_task
def store_feed(feed_data, group_id, use_celery=False, is_check=False, is_check_comment=False):
    """
    This method stores a feed.

    :param feed_data: feed data(dictionary)
    :param group_id: post's group id
    :param use_celery: use celery?
    :param is_check: is check?
    :param is_check_comment: is check comment?
    :return:
    """
    # save post from feeds
    group = Group.objects.filter(id=group_id)[0]
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
                if use_celery:
                    store_attachment.delay(attachment_data=attachment_data, post_id=post.id, use_celery=use_celery)
                else:
                    store_attachment(attachment_data=attachment_data, post_id=post.id, use_celery=use_celery)

        # save user activity
        UserActivity.add_post_count(user=post.user, group=post.group)
    else:
        post = Post.objects.filter(id=post_id)[0]

        if is_check or post.is_updated(feed_data.get('updated_time')):

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
        elif is_check_comment:
            post_comments = feed_data.get('comments')
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
        if use_celery:
            store_comment.delay(comment_data=comment_data, post_id=post_id, group_id=group.id, use_celery=use_celery)
        else:
            store_comment(comment_data=comment_data, post_id=post_id, group_id=group.id, use_celery=use_celery)

    return True


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
        if 'owner' in group_data:
            group.owner = store_user(group_data.get('owner').get('id'), group_data.get('owner').get('name'), group)
        group.save()
        logger.info('Saved group: %s', group)
    else:
        group = Group.objects.filter(id=group_id)[0]
        group.name = group_data.get('name')
        group.description = group_data.get('description')
        group.updated_time = group_data.get('updated_time')
        group.privacy = group_data.get('privacy')
        if 'owner' in group_data:
            group.owner = store_user(group_data.get('owner').get('id'), group_data.get('owner').get('name'), group)
        group.save()
        logger.info('Update group updated_time: %s', group.id)
    return group


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
def store_group_feed(group_id, query, use_celery=False, is_whole=False):
    """
    This method is storing group's feeds by using facebook group api.
    If you want to get whole data, put that 'is_whole' is true.

    :param group_id: param group_id: group id for getting feeds
    :param query: query for facebook graph api
    :param use_celery: use celery?
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

    while query is not None:
        feeds = []
        try:
            query = fb_request.feed(group, query, feeds)
        except Exception as e:
            logger.error('Fail to request by exception : %s', e)
            try:
                query = fb_request.feed(group, query, feeds)
            except Exception as e:
                logger.error('Fail to request again by exception : %s', e)

        for feed in feeds:
            try:
                store_feed(feed, group.id, use_celery)
            except Exception as e:
                logger.error('Fail to store by exception : %s', e)
                try:
                    store_feed(feed, group.id, use_celery)
                except Exception as e:
                    logger.error('Fail to store again by exception : %s', e)
        if not is_whole:
            break

    group.is_stored = True
    group.save()
    check_cp_cnt_group(group)

    end_time = timezone.datetime.now().replace(microsecond=0)
    logger.info('End time : %s', end_time)
    logger.info('Time difference : %s', end_time - start_time)
    logger.info('=== End saving %s feed ===', group_id)


@shared_task
def update_group_feed(group_id, query, use_celery=False, is_whole=False):
    """
    This method is updating group's feeds by using facebook group api.
    If you want to get whole data, put that 'is_whole' is true.

    :param group_id: param group_id: group id for getting feeds
    :param query: query for facebook graph api
    :param use_celery: use celery?
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

    check_cp_cnt_group(group)

    if not group.is_stored:
        logger.info('=== Fail to update %s feed (Group is not stored) ===', group_id)
        return False

    if not group.is_updated(updated_time):
        logger.info('=== Fail to update %s feed (Already updated) ===', group_id)
        return False

    if group.privacy == "CLOSED":
        logger.info('=== Fail to update %s feed (Group is closed) ===', group_id)
        return False

    store_group(group_data)

    while query is not None:
        feeds = []
        try:
            query = fb_request.feed(group, query, feeds)
        except Exception as e:
            logger.error('Fail to request by exception : %s', e)
            try:
                query = fb_request.feed(group, query, feeds)
            except Exception as e:
                logger.error('Fail to request again by exception : %s', e)

        for feed in feeds:
            try:
                res = store_feed(feed, group.id)
            except Exception as e:
                logger.error('Fail to update by exception : %s', e)
                try:
                    res = store_feed(feed, group.id)
                except Exception as e:
                    logger.error('Fail to update again by exception : %s', e)
            if not res:
                return True
        if not is_whole:
            break

    end_time = timezone.datetime.now().replace(microsecond=0)
    logger.info('End time : %s', end_time)
    logger.info('Time difference : %s', end_time - start_time)
    logger.info('=== End updating %s feed ===', group_id)
    return True


@shared_task
def update_groups_feed(query, use_celery=False, is_whole=False):
    """
    This method is updating group's feeds by using facebook group api for celery schedule.
    If you want to get whole data, put that 'is_whole' is true.

    :param query: query for facebook graph api
    :param use_celery: use celery?
    :param is_whole: whole or parts
    :return:
    """
    logger.info('=== Start updating groups ===')
    start_time = timezone.datetime.now().replace(microsecond=0)
    logger.info('Start time : %s', start_time)
    groups = Group.objects.values('id')

    for group in groups:
        update_group_feed.delay(group.get('id'), query, use_celery, is_whole)

    end_time = timezone.datetime.now().replace(microsecond=0)
    logger.info('End time : %s', end_time)
    logger.info('Time difference : %s', end_time - start_time)
    logger.info('=== End updating groups ===')


@shared_task
def check_group_feed(group_id, query, use_celery=False, is_whole=False):
    """
    This method is checking group's feeds by using facebook group api.
    If you want to get whole data, put that 'is_whole' is true.

    :param group_id: param group_id: group id for getting feeds
    :param query: query for facebook graph api
    :param use_celery: use celery?
    :param is_whole: whole or parts
    :return:
    """
    logger.info('=== Start checking %s feed ===', group_id)
    start_time = timezone.datetime.now().replace(microsecond=0)
    logger.info('Start time : %s', start_time)

    group = Group.objects.filter(id=group_id)[0]

    if group.privacy == "CLOSED":
        logger.info('=== Fail to check %s feed (Group is closed) ===', group_id)
        return False

    while query is not None:
        feeds = []
        try:
            query = fb_request.feed(group, query, feeds)
        except Exception as e:
            logger.error('Fail to request by exception : %s', e)
            try:
                query = fb_request.feed(group, query, feeds)
            except Exception as e:
                logger.error('Fail to request again by exception : %s', e)

        for feed in feeds:
            try:
                store_feed(feed, group.id, use_celery, True)
            except Exception as e:
                logger.error('Fail to check by exception : %s', e)
                try:
                    store_feed(feed, group.id, use_celery, True)
                except Exception as e:
                    logger.error('Fail to check again by exception : %s', e)
        if not is_whole:
            break

    group.is_stored = True
    group.save()
    check_cp_cnt_group(group)

    end_time = timezone.datetime.now().replace(microsecond=0)
    logger.info('End time : %s', end_time)
    logger.info('Time difference : %s', end_time - start_time)
    logger.info('=== End check %s feed ===', group_id)


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
        UserActivity.sub_post_count(user=content.user, group=content.group)

        comments = Comment.objects.filter(post=content)
        if comments:
            for comment in comments:
                deleted_comment = DeletedComment.create(comment)
                deleted_comment.save()

            for comment in comments:
                UserActivity.sub_comment_count(user=comment.user, group=comment.group)
                comment.delete()
    else:
        deleted_comment = DeletedComment.create(content)
        deleted_comment.save()
        UserActivity.sub_comment_count(user=content.user, group=content.group)

        child_comments = Comment.objects.filter(parent=content)
        if child_comments:
            for child_comment in child_comments:
                deleted_comment = DeletedComment.create(child_comment)
                deleted_comment.save()

            for child_comment in child_comments:
                UserActivity.sub_comment_count(user=child_comment.user, group=child_comment.group)
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
        if 'Unsupported delete request' not in e.__str__():
            return False, e.__str__()

    return delete_group_content(object_id, model)


@shared_task
def check_group_comments(group_id, query, use_celery=False, is_whole=False):
    """
    This method is storing group's comments by using facebook group api.
    If you want to get whole data, put that 'is_whole' is true.

    :param group_id: param group_id: group id for getting feeds
    :param query: query for facebook graph api
    :param use_celery: use celery?
    :param is_whole: whole or parts
    :return:
    """
    logger.info('=== Start checking %s comments ===', group_id)
    start_time = timezone.datetime.now().replace(microsecond=0)
    logger.info('Start time : %s', start_time)

    group = Group.objects.filter(id=group_id)[0]

    if group.privacy == "CLOSED":
        logger.info('=== Fail to check %s comments (Group is closed) ===', group_id)
        return False

    while query is not None:
        feeds = []
        try:
            query = fb_request.feed(group, query, feeds)
        except Exception as e:
            logger.error('Fail to request by exception : %s', e)
            try:
                query = fb_request.feed(group, query, feeds)
            except Exception as e:
                logger.error('Fail to request again by exception : %s', e)

        for feed in feeds:
            try:
                store_feed(feed, group.id, use_celery, False, True)
            except Exception as e:
                logger.error('Fail to check by exception : %s', e)
                try:
                    store_feed(feed, group.id, use_celery, False, True)
                except Exception as e:
                    logger.error('Fail to check again by exception : %s', e)
        if not is_whole:
            break

    group.is_stored = True
    group.save()
    check_cp_cnt_group(group)

    end_time = timezone.datetime.now().replace(microsecond=0)
    logger.info('End time : %s', end_time)
    logger.info('Time difference : %s', end_time - start_time)
    logger.info('=== End checking %s comments ===', group_id)
