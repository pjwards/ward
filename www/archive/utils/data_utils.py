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
""" Provides data utils for checking correct data """

from django.db import connection

from archive.fb.fb_request import FBRequest
from archive.models import *

__author__ = "Donghyun Seo"
__copyright__ = "Copyright ⓒ 2015, All rights reserved."
__email__ = "egaoneko@naver.com"


def dict_fetchall(cursor):
    """
    Return all rows from a cursor as a dict

    :param cursor: cursor
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def update_user_activity():
    """
    Update user all activity.

    :return:
    """
    cursor = connection.cursor()
    groups = Group.objects.all()

    for group in groups:
        cursor.execute(
            """
            SELECT
                UG.fbuser_id as id,
                (SELECT count(*) FROM archive_post WHERE group_id = %s AND user_id = UG.fbuser_id) as p_count,
                (SELECT count(*) FROM archive_comment WHERE group_id = %s AND user_id = UG.fbuser_id) as c_count
            FROM
                archive_fbuser_groups as UG
            INNER JOIN archive_fbuser as U
            ON UG.fbuser_id = U.id
            WHERE UG.group_id = %s
            ORDER BY U.name;
            """, [group.id, group.id, group.id])
        rows = dict_fetchall(cursor)

        for row in rows:
            user = FBUser.objects.get(id=row.get('id'))
            print("group={} | user={}".format(group.id, user.id))

            if not UserActivity.objects.filter(user=user, group=group).exists():
                user_activity = UserActivity(user=user, group=group,
                                             post_count=row.get('p_count'), comment_count=row.get('c_count'))
                user_activity.save()
            else:
                user_activity = UserActivity.objects.filter(user=user, group=group)[0]
                user_activity.post_count = row.get('p_count')
                user_activity.comment_count = row.get('c_count')
                user_activity.save()


def check_users_name():
    """
    Check users name

    :return:
    """
    print('=== Start checking users name ===')

    # Check Korean and English
    users = FBUser.objects.filter(name__iregex=r'[^ \-a-zA-Z0-9\u3131-\u3163\uac00-\ud7a3]+')
    print('Checked Users : %s' % users.count())

    i = 1
    for user in users:
        print('=' * 10 + str(i) + '=' * 10)
        i += 1

        print('Start checking %s name' % user.name)
        check_user_name(user.id)
        print('End checking %s name' % user.name)
    print('=== End checking users name ===')


def check_user_name(user_id):
    """
    Check name about each user by using posts or comments

    :param user_id: user id
    :return:
    """
    user = FBUser.objects.get(id=user_id)
    contents = Post.objects.filter(user=user)

    if contents:
        if not check_user_from_contents(user, contents):
            contents = Comment.objects.filter(user=user)
            check_user_from_contents(user, contents)
    else:
        contents = Comment.objects.filter(user=user)
        check_user_from_contents(user, contents)


def check_user_from_contents(user, contents):
    """
    Check name about each user by using posts or comments

    :param user: user
    :param contents: contents
    :return:
    """
    fb_request = FBRequest()
    for content in contents:
        try:
            result = fb_request.graph.request(content.id, {'field': 'from'}).get('from')
        except Exception as e:
            print('Fail to request by exception : %s', e)
            continue

        print(result)

        if result:
            if 'name' in result:
                name = result.get('name')
            if name != user.name:
                print('Change name from %s to %s' % (user.name, name))
                user.name = name
                user.save()
                return True
            elif name == user.name:
                print('Name is same. (%s)' % user.name)
                return True
    return False
