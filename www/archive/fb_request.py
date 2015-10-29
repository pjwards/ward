import facebook
from django.conf import settings
from urllib.parse import urlparse, unquote
import logging

__author__ = "Donghyun Seo"
__copyright__ = "Copyright ⓒ 2015, All rights reserved."
__email__ = "egaoneko@naver.com"

logger = logging.getLogger(__name__)


class FBRequest:
    """
    FBRequest gets data from facebook by using graph api and facebook-sdk.
    """
    def __init__(self):

        app_id = settings.FB_APP_ID
        app_secret = settings.FB_APP_SECRET
        app_version = settings.FB_APP_VERSION

        self.graph = facebook.GraphAPI(
            access_token=facebook.GraphAPI().get_app_access_token(app_id, app_secret),
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
            re = self.graph.request(group_id, args={'fields': 'id,name,description,updated_time,privacy'})
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
