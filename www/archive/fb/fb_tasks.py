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
""" Provides a task by using fb_request """

import logging

import time
from facebook import GraphAPIError

from archive.fb.fb_request import FBRequest
from archive.models import *
from archive.utils.utils import is_connected

logger = logging.getLogger(__name__)

if is_connected():
    fb_request = FBRequest()


def store_user(user_id, user_name, group):
    """
    This method stores a user.

    :param user_id: user id
    :param user_name:  user name
    :param group: user group
    :return: user model
    """
    user = FBUser.objects.filter(id=user_id)
    if not user:
        # save user
        user = FBUser(id=user_id, name=user_name)
        user.picture = fb_request.user_picture(user_id)
        user.save()
        logger.info('Saved user: %s', user.id)
    else:
        user = user[0]
        is_update = user.is_update()

        if is_update:
            is_change = False
            picture = fb_request.user_picture(user_id)
            if user.name != user_name:
                is_change = True
                user.name = user_name
            elif user.picture != picture:
                is_change = True
                user.picture = picture
            if is_change:
                logger.info('Update user: %s', user.id)
            user.updated_time = timezone.now()
            user.save()

    user.groups.add(group)

    return user


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
                store_attachment(attachment_data=subattachment_data, post=post)

            if comment is not None:
                store_attachment(attachment_data=subattachment_data, comment=comment)


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

        # save attachment
        if 'attachment' in comment_data:
            store_attachment(attachment_data=comment_data.get('attachment'), comment=comment)

        # save user activity
        UserActivity.add_comment_count(user=comment.user, group=comment.group)

        # save month comment
        MonthComment.create(comment=comment)
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


def store_comments(post_comments, post, group):
    """
    This method stores post's comments

    :param post_comments: post's comments
    :param post: post
    :param group: group
    :return:
    """
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


def store_feed(feed_data, group, is_store_comment=False, is_check=False):
    """
    This method stores a feed.

    :param feed_data: feed data(dictionary)
    :param group: post's group
    :param is_store_comment: do store comments?
    :param is_check: is check?
    :return:
    """
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

        # save user activity
        UserActivity.add_post_count(user=post.user, group=post.group)

        # save month post
        MonthPost.create(post=post)
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
        else:
            return False

    if is_store_comment:
        store_comments(post_comments, post, group)

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


def store_group_feed(group, query):
    """
    This method is storing group's feeds by using facebook group api.

    :param group: group for getting feeds
    :param query: query for facebook graph api
    :return:
    """
    logger.info('=== Start saving %s feed ===', group.id)

    is_check = False
    if not GroupStoreList.objects.filter(group=group).exists():
        group_store_list = GroupStoreList(group=group, query=query)
        group_store_list.save()
    else:
        group_store_list = GroupStoreList.objects.filter(group=group)[0]

        if group_store_list.query:
            query = group_store_list.query

            if group_store_list.status != 'finish':
                is_check = True

    if group.privacy == "CLOSED":
        logger.info('=== Fail to save %s feed (Group is closed) ===', group.id)
        return False

    error_cnt = 0
    while query is not None:
        feeds = []
        try:
            query = fb_request.feed(group.id, query, feeds)
        except Exception as e:
            logger.error('Fail to request by exception : %s', e)

            error_cnt += 1
            if error_cnt > 2:
                error_list = GroupArchiveErrorList.objects.filter(group=group)
                if error_list:
                    error_list[0].error_count += 1
                    error_list[0].message = '[store] : ' + str(e)
                    error_list[0].query = group.id + query
                    error_list[0].save()
                else:
                    GroupArchiveErrorList(group=group, query=group.id + query, message='[store] : ' + str(e)).save()
                return

        for feed in feeds:
            try:
                store_feed(feed, group, False, is_check)
            except Exception as e:
                logger.error('Fail to store by exception : %s', e)

        # save query for continue saving
        group_store_list.query = query
        group_store_list.save()
        check_cp_cnt_group(group)

    # finish save
    group_store_list.query = ''
    group_store_list.end_time = timezone.now()
    group_store_list.status = 'finish'
    group_store_list.save()

    logger.info('=== End saving %s feed ===', group.id)


def update_group_feed(group, query):
    """
    This method is updating group's feeds by using facebook group api.

    :param group: group for getting feeds
    :param query: query for facebook graph api
    :return: success?
    """
    logger.info('=== Start updating %s feed ===', group.id)

    try:
        group_data = fb_request.group(group.id)
    except Exception as e:
        logger.info('Fail to get group data by exception : %s', e)
        return False

    updated_time = group_data.get('updated_time')
    group = Group.objects.filter(id=group.id)[0]

    # check group status for update
    if group.privacy == "CLOSED":
        logger.info('=== Fail to update %s feed (Group is closed) ===', group.id)
        return False
    if not group.is_stored:
        logger.info('=== Fail to update %s feed (Group is not stored) ===', group.id)
        return False
    if not group.is_updated(updated_time):
        logger.info('=== Fail to update %s feed (Already updated) ===', group.id)
        return False

    updated_time_backup = group.updated_time
    store_group(group_data)

    error_cnt = 0
    while query is not None:
        feeds = []
        try:
            query = fb_request.feed(group.id, query, feeds)
        except Exception as e:
            logger.error('Fail to request by exception : %s', e)

            error_cnt += 1
            if error_cnt > 2:
                error_list = GroupArchiveErrorList.objects.filter(group=group)
                if error_list:
                    error_list[0].error_count += 1
                    error_list[0].message = '[update] : ' + str(e)
                    error_list[0].query = group.id + query
                    error_list[0].save()

                    if error_list[0].error_count >= 100:
                        group.is_stored = False
                        group.save()
                else:
                    GroupArchiveErrorList(group=group, query=group.id + query, message='[update] : ' + str(e)).save()

                group.updated_time = updated_time_backup
                group.save()
                return False

        for feed in feeds:
            try:
                res = store_feed(feed, group, True)
            except Exception as e:
                logger.error('Fail to update by exception : %s', e)

            # if post isn't updated, exit
            if not res:
                check_cp_cnt_group(group)
                store_group(group_data)
                return True

    check_cp_cnt_group(group)
    store_group(group_data)
    logger.info('=== End updating %s feed ===', group.id)
    return True


def check_post_comment(post, query):
    """
    This method is storing post's comments by using facebook group api.

    :param post: post for getting comments
    :param query: query for facebook graph api
    :return:
    """
    logger.info('=== Start checking %s comments ===', post.id)

    error_cnt = 0
    while query is not None:
        comments = []
        try:
            query = fb_request.comments(post.id, query, comments)
        except Exception as e:
            logger.error('Fail to request by exception : %s', e)

            error_cnt += 1
            if error_cnt > 2:
                error_list = GroupArchiveErrorList.objects.filter(group=post.group)
                if error_list:
                    error_list[0].error_count += 1
                    error_list[0].message = '[check] : ' + str(e)
                    error_list[0].query = post.id + query
                    error_list[0].save()
                else:
                    GroupArchiveErrorList(group=post.group, query=post.id + query, message='[check] : ' + str(e)).save()
                return

        for comment in comments:
            try:
                store_comment(comment_data=comment, post=post, group=post.group)
            except Exception as e:
                logger.error('Fail to check by exception : %s', e)

    check_cp_cnt_group(post.group)
    logger.info('=== End checking %s comments ===', post.id)


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
