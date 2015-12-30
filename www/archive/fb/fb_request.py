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
""" Provides a class for using facebook graph api """

import facebook
from django.conf import settings
from urllib.parse import urlparse, unquote
import logging

logger = logging.getLogger(__name__)


class FBRequest:
    """
    FBRequest gets data from facebook by using graph api and facebook-sdk.
    """
    def __init__(self, access_token=None):

        app_id = settings.FB_APP_ID
        app_secret = settings.FB_APP_SECRET
        app_version = settings.FB_APP_VERSION

        if access_token is None:
            self.graph = facebook.GraphAPI(
                access_token=facebook.GraphAPI().get_app_access_token(app_id, app_secret),
                version=app_version
            )
        else:
            self.graph = facebook.GraphAPI(
                access_token=access_token,
                version=app_version
            )

    def feed(self, group, query, feeds):
        """
        This method gets feeds.

        :param group: group to find feeds
        :param query: details to find feeds
        :param feeds: list of feed data
        :return:
        """
        re = self.graph.request(group.id + query)

        if re.get('feed') is not None:
            re = re.get('feed')

        len_data = len(re.get('data'))
        if len_data == 0:
            return None

        logger.info('Get Feeds: %d', len_data)
        feeds += re.get('data')
        next_query = "/feed?" + unquote(urlparse(re.get('paging').get('next')).query)

        return next_query

    def comments(self, post, query, comments):
        """
        This method gets comments.

        :param post: post to find comments
        :param query: details to find comments
        :param comments: list of comments data
        :return:
        """
        re = self.graph.request(post.id + query)

        if re.get('comments') is not None:
            re = re.get('comments')

        len_data = len(re.get('data'))
        if len_data == 0:
            return None

        logger.info('Get Feeds: %d', len_data)
        comments += re.get('data')

        next_query = None
        if 'next' in re.get('paging'):
            next_query = "/comments?" + unquote(urlparse(re.get('paging').get('next')).query)
        return next_query

    def comment(self, query, comments):
        """
        This method gets comments

        :param query: details to find comments
        :param comments: list of comment data
        :return:
        """
        re = self.graph.request(query)

        len_data = len(re.get('data'))
        if len_data == 0:
            return None

        logger.info('Get Comments: %d', len_data)
        comments += re.get('data')

        if 'next' in re.get('paging'):
            next_query = self.get_comment_next_query(re.get('paging').get('next'))
        else:
            return None

        return next_query

    @staticmethod
    def get_comment_next_query(url):
        """
        This method gets a next query for comments.

        :param url: next url
        :return:
        """
        url_parse = urlparse(unquote(url))
        url_path_list = url_parse.path.split('/')
        url_path = "/" + url_path_list[2] + "/" + url_path_list[3] + "?"
        url_query = url_parse.query
        return url_path + url_query

    def group(self, group_id):
        """
        This method gets a group.

        :param group_id: group id to find group
        :return: group data
        """
        try:
            re = self.graph.request(group_id, args={'fields': 'id,name,description,updated_time,privacy,owner'})
        except facebook.GraphAPIError as e:
            logger.info('Fail to get group')
            return None

        logger.info('Get Group: %s', group_id)

        return re

    def user_picture(self, user_id):
        """
        This method gets a user picture.

        :param user_id: user id to get picture
        :return: picture url
        """
        re = self.graph.request(user_id + "/picture")

        logger.info('Get user picture: %s', user_id)
        return re.get('url')

    def delete_object(self, object_id):
        """
        Delete some object

        :param object_id: object id
        :return:
        """
        self.graph.delete_object(object_id)
        logger.info('Delete object: %s', object_id)

    def validate_token(self):
        """
        Validate token

        :return:
        """
        try:
            self.graph.request("me")
            return True, None
        except facebook.GraphAPIError as e:
            logger.info('Fail to access')
            return False, e.__str__()

