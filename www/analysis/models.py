from django.db import models
from archive.models import Group

__author__ = 'jeonjiseong'


class SpamContentList(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    group = models.ForeignKey(Group)
    text = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, default="temp")        # deleted, temp


class SpamWordList(models.Model):
    group = models.ForeignKey(Group)
    word = models.CharField(max_length=255)
    count = models.IntegerField(default=1)
    status = models.CharField(max_length=10, default="temp")        # deleted, temp
    # feature -> word, url


