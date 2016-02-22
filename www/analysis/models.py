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
""" Sets models """

from django.db import models
from archive.models import Group, FBUser, Comment, Post


class SpamList(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    group = models.ForeignKey(Group, related_name='spamlist')
    user = models.ForeignKey(FBUser, related_name='spamlist')
    message = models.TextField(null=True, blank=True)
    time = models.DateTimeField()
    status = models.CharField(max_length=10, default='temp')        # deleted, temp

    def __str__(self):
        return self.id


class SpamWordList(models.Model):
    group = models.ForeignKey(Group, related_name='spamwords')
    word = models.CharField(max_length=255)
    count = models.IntegerField(default=1)
    status = models.CharField(max_length=10, default='temp')          # temp, filter, user, deleted


class ArchiveAnalysisWord(models.Model):
    word = models.CharField(max_length=255)
    count = models.IntegerField(default=1)
    status = models.CharField(max_length=10, default='temp')
    group = models.ForeignKey(Group, related_name='archivewords')
    # word weight with likes and comments


class AnticipateArchive(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    group = models.ForeignKey(Group, related_name='antiArchives')
    user = models.ForeignKey(FBUser, related_name='antiArchives')
    message = models.TextField(null=True, blank=True)
    time = models.DateTimeField()
    status = models.CharField(max_length=10, default='temp')
    # type


class AnalysisDBSchema(models.Model):
    group = models.ForeignKey(Group, related_name='analysisSchema')
    avgpostlike = models.IntegerField(default=0)
    avgpostcomment = models.IntegerField(default=0)
    avgcomtlike = models.IntegerField(default=0)
    avgcomtcomment = models.IntegerField(default=0)
    lastupdatetime = models.DateTimeField()
