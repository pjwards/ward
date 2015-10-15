__author__ = "Donghyun Seo"
__copyright__ = "Copyright ⓒ 2015, All rights reserved."
__email__ = "egaoneko@naver.com"


FEED_QUERY = '?fields=feed.limit(100){' \
             'message,' \
             'from,' \
             'created_time,' \
             'updated_time,' \
             'picture,' \
             'attachments{url,title,description,type,media,subattachments},' \
             'comments.limit(100).summary(true){' \
                'id,' \
                'from,' \
                'created_time,' \
                'message,' \
                'like_count,' \
                'attachment,' \
                'comments.limit(100).summary(true){id,from,created_time,message,like_count,attachment,parent}},' \
             'likes.summary(true),' \
             'shares}'

COMMENTS_QUERY = '?fields=comments.limit(100).summary(true){' \
                 'id,' \
                 'from,' \
                 'created_time,' \
                 'message,' \
                 'like_count,' \
                 'attachment,' \
                 'comments.limit(100).summary(true){id,from,created_time,message,like_count,attachment,parent}}'

