from django.db import models

__author__ = "Donghyun Seo"
__copyright__ = "Copyright ⓒ 2015, All rights reserved."
__email__ = "egaoneko@naver.com"


class User(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Group(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    updated_time = models.DateTimeField()
    privacy = models.CharField(max_length=30)
    is_stored = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(User)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    message = models.TextField(null=True, blank=True)
    picture = models.CharField(max_length=255, null=True, blank=True)
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)

    def __str__(self):
        return self.message


class Comment(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(User)
    created_time = models.DateTimeField()
    message = models.TextField(null=True, blank=True)
    like_count = models.IntegerField(default=0)
    post = models.ForeignKey(Post)
    parent = models.ForeignKey('Comment', null=True)

    def __str__(self):
        return self.message


class Media(models.Model):
    height = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    src = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.src


class Attachment(models.Model):
    post = models.ForeignKey(Post, null=True)
    comment = models.ForeignKey(Comment, null=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=30, null=True, blank=True)
    # photo, share, unavailable, album(sub), video_autoplay, multi_share(sub), video_share_youtube, note
    media = models.ForeignKey(Media, null=True)

    def __str__(self):
        return self.url
