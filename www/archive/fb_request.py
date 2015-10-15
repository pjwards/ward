import facebook
from django.conf import settings
from urllib.parse import urlparse, unquote
import logging

__author__ = 'seodonghyeon'

logger = logging.getLogger(__name__)


class FBRequest:
    def __init__(self):

        app_id = settings.FB_APP_ID
        app_secret = settings.FB_APP_SECRET
        app_version = settings.FB_APP_VERSION

        self.graph = facebook.GraphAPI(
            access_token=facebook.GraphAPI().get_app_access_token(app_id, app_secret),
            version=app_version
        )

    def feed(self, group_id, query, feeds):
        re = self.graph.request(group_id + query)

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
        re = self.graph.request(query)

        len_data = len(re.get('data'))
        if len_data == 0:
            return None

        logger.info('Get Feeds: %d', len_data)
        comments += re.get('data')

        if 'next' in re.get('paging'):
            next_query = self.get_comment_next_query(re.get('paging').get('next'))
        else:
            return None

        return next_query

    @staticmethod
    def get_comment_next_query(url):
        url_parse = urlparse(unquote(url))
        url_path_list = url_parse.path.split('/')
        url_path = "/" + url_path_list[2] + "/" + url_path_list[3] + "?"
        url_query = url_parse.query
        return url_path + url_query

