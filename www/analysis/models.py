from django.db import models


class SpamContent(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    text = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, default="temp")        # deleted, temp


class SpamList(models.Model):
    word = models.CharField(max_length=255, primary_key=True)
    count = models.IntegerField(default=1)
    status = models.CharField(max_length=10, default="temp")        # deleted, temp
    # feature -> word, url