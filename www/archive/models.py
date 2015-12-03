from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User as DjangoUser
from mezzanine.core.managers import SearchableManager

__author__ = "Donghyun Seo"
__copyright__ = "Copyright ⓒ 2015, All rights reserved."
__email__ = "egaoneko@naver.com"


def get_different_time(time):
    """
    Get different time from input time

    :param time: time for compare
    :return: days or hours or minutes or seconds ago
    """
    now = timezone.now()

    diff = now - time
    s = diff.total_seconds()
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)

    if diff.days > 0:
        return str(int(diff.days)) + " days ago"
    elif hours > 0:
        return str(int(hours)) + " hours ago"
    elif minutes > 0:
        return str(int(minutes)) + " minutes ago"
    else:
        return str(int(seconds)) + " seconds ago"


class Group(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    updated_time = models.DateTimeField()
    privacy = models.CharField(max_length=30)
    is_stored = models.BooleanField(default=False)
    post_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    owner = models.ForeignKey('User', null=True, related_name='group_owner')

    objects = SearchableManager()
    search_fields = ("name",)

    def __str__(self):
        return self.id

    def is_updated(self, new_updated_time):
        """
        Check group is updated.

        :param new_updated_time: json datetime
        :return: True is updated and False is not updated
        """
        return self.updated_time.strftime('%Y-%m-%dT%H:%M:%S') != new_updated_time.split('+')[0]

    def get_diff_time(self):
        """
        Get different time from updated time

        :return: different time
        """
        return get_different_time(self.updated_time)


class User(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    picture = models.CharField(max_length=2083, null=True, blank=True)
    groups = models.ManyToManyField(Group)

    objects = SearchableManager()
    search_fields = ("name",)

    def __str__(self):
        return self.id


class Post(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(User, related_name='posts')
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    message = models.TextField(null=True, blank=True)
    picture = models.CharField(max_length=2083, null=True, blank=True)
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    group = models.ForeignKey(Group, related_name='posts')
    is_show = models.BooleanField(default=True)

    objects = SearchableManager()
    search_fields = ("message",)

    def __str__(self):
        return self.id

    def is_updated(self, new_updated_time):
        """
        Check post is updated.

        :param new_updated_time: json datetime
        :return: True is updated and False is not updated
        """
        return self.updated_time.strftime('%Y-%m-%dT%H:%M:%S') != new_updated_time.split('+')[0]

    def get_diff_cre_time(self):
        """
        Get different time from created time

        :return: different time
        """
        return get_different_time(self.created_time)

    def get_diff_upe_time(self):
        """
        Get different time from updated time

        :return: different time
        """
        return get_different_time(self.updated_time)


class Comment(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(User, related_name='comments')
    created_time = models.DateTimeField()
    message = models.TextField(null=True, blank=True)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    post = models.ForeignKey(Post, related_name='comments')
    parent = models.ForeignKey('Comment', null=True, related_name='comments')
    group = models.ForeignKey(Group, related_name='comments')
    is_show = models.BooleanField(default=True)

    objects = SearchableManager()
    search_fields = ("message",)

    def __str__(self):
        return self.id

    def get_diff_cre_time(self):
        """
        Get different time from created time

        :return: different time
        """
        return get_different_time(self.created_time)


class Media(models.Model):
    height = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    src = models.CharField(max_length=2083, null=True, blank=True)


class Attachment(models.Model):
    post = models.ForeignKey(Post, null=True, related_name='attachments')
    comment = models.ForeignKey(Comment, null=True, related_name='attachments')
    url = models.CharField(max_length=2083, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=30, null=True, blank=True)
    # photo, share, unavailable, album(sub), video_autoplay, multi_share(sub), video_share_youtube, note
    media = models.ForeignKey(Media, null=True, related_name='media')

    objects = SearchableManager()
    search_fields = ("description",)


class Blacklist(models.Model):
    group = models.ForeignKey(Group, related_name='blacklist')
    user = models.ForeignKey(User, related_name='blacklist')
    count = models.IntegerField(default=0)
    updated_time = models.DateTimeField(auto_now=True)


class Report(models.Model):
    post = models.ForeignKey(Post, null=True, related_name='reports')
    comment = models.ForeignKey(Comment, null=True, related_name='reports')
    group = models.ForeignKey(Group, related_name='reports')
    user = models.ForeignKey(User, related_name='reports')
    status = models.CharField(max_length=30, default='new')
    updated_time = models.DateTimeField(auto_now=True)


class DeletedPost(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(User, related_name='delete_posts')
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    message = models.TextField(null=True, blank=True)
    picture = models.CharField(max_length=2083, null=True, blank=True)
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    group = models.ForeignKey(Group, related_name='delete_posts')

    objects = SearchableManager()
    search_fields = ("message",)

    def __str__(self):
        return self.id

    def is_updated(self, new_updated_time):
        """
        Check post is updated.

        :param new_updated_time: json datetime
        :return: True is updated and False is not updated
        """
        return self.updated_time.strftime('%Y-%m-%dT%H:%M:%S') != new_updated_time.split('+')[0]

    def get_diff_cre_time(self):
        """
        Get different time from created time

        :return: different time
        """
        return get_different_time(self.created_time)

    def get_diff_upe_time(self):
        """
        Get different time from updated time

        :return: different time
        """
        return get_different_time(self.updated_time)

    @classmethod
    def create(cls, post):
        return cls(id=post.id, user=post.user, created_time=post.created_time, updated_time=post.updated_time,
                   message=post.message, picture=post.picture, comment_count=post.comment_count,
                   like_count=post.like_count, share_count=post.share_count, group=post.group)


class DeletedComment(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(User, related_name='delete_comments')
    created_time = models.DateTimeField()
    message = models.TextField(null=True, blank=True)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    post = models.CharField(max_length=50)
    parent = models.CharField(max_length=20, null=True)
    group = models.ForeignKey(Group, related_name='delete_comments')

    objects = SearchableManager()
    search_fields = ("message",)

    def __str__(self):
        return self.id

    def get_diff_cre_time(self):
        """
        Get different time from created time

        :return: different time
        """
        return get_different_time(self.created_time)


    @classmethod
    def create(cls, comment):
        if comment.parent:
            parent = comment.parent.id
        else:
            parent = None
        return cls(id=comment.id, user=comment.user, created_time=comment.created_time, message=comment.message,
                   like_count=comment.like_count, comment_count=comment.comment_count, post=comment.post.id,
                   parent=parent, group=comment.group)


class Ward(models.Model):
    user = models.ForeignKey(DjangoUser, related_name='wards')
    group = models.ForeignKey(Group, related_name='wards')
    post = models.ForeignKey(Post, null=True, related_name='wards')
    comment = models.ForeignKey(Comment, null=True, related_name='wards')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now_add=True)

    def is_updated(self, new_updated_time):
        """
        Check post is updated.

        :param new_updated_time: json datetime
        :return: True is updated and False is not updated
        """
        return self.updated_time.strftime('%Y-%m-%dT%H:%M:%S') != new_updated_time.split('+')[0]
