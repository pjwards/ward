FEED_QUERY = '?fields=feed.limit(%d){' \
             'message,' \
             'from,' \
             'created_time,' \
             'updated_time,' \
             'picture,' \
             'attachments{url,title,description,type,media,subattachments},' \
             'comments.limit(%d).summary(true){' \
                'id,' \
                'from,' \
                'created_time,' \
                'message,' \
                'like_count,' \
                'attachment,' \
                'comments.limit(%d).summary(true){id,from,created_time,message,like_count,attachment,parent}},' \
             'likes.summary(true),' \
             'shares}'

COMMENTS_QUERY = '?fields=comments.limit(%d).summary(true){' \
                 'id,' \
                 'from,' \
                 'created_time,' \
                 'message,' \
                 'like_count,' \
                 'attachment,' \
                 'comments.limit(%d).summary(true){id,from,created_time,message,like_count,attachment,parent}}'


def get_feed_query(feed_limit=100, comments_limit=100):
    """
    This method return query for feed.

    :param feed_limit: how many feeds?
    :param comments_limit: how many comment?
    :return: feed query
    """
    return FEED_QUERY % (feed_limit, comments_limit, comments_limit)


def get_comment_query(comments_limit=100, child_comments_limit=100):
    """
    This method return query for comment.

    :param comments_limit: how many comments?
    :param child_comments_limit: how many child comment?
    :return: feed query
    """
    return COMMENTS_QUERY % (comments_limit, child_comments_limit)

