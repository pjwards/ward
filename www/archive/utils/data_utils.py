from django.db import connection

from archive.models import FBUser, Group, UserActivity

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
