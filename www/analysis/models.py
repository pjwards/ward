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

from archive.models import *


class SpamList(models.Model):
    """
    List of Spams
    """
    id = models.CharField(max_length=50, primary_key=True)
    group = models.ForeignKey(Group, related_name='spamlist')
    user = models.ForeignKey(FBUser, related_name='spamlist')
    message = models.TextField(null=True, blank=True)
    time = models.DateTimeField()
    status = models.CharField(max_length=10, default='temp')        # deleted, temp

    def __str__(self):
        return self.id


class SpamWordList(models.Model):
    """
    Word list of spam
    """
    group = models.ForeignKey(Group, related_name='spamwords')
    word = models.CharField(max_length=255)
    count = models.IntegerField(default=1)
    status = models.CharField(max_length=10, default='temp')          # temp, filter, user, deleted


class ArchiveAnalysisWord(models.Model):
    """
    Word list of analyzed posts
    """
    group = models.ForeignKey(Group, related_name='archivewords')
    word = models.CharField(max_length=255)
    count = models.IntegerField(default=1)
    likenum = models.IntegerField(default=0)
    commentnum = models.IntegerField(default=0)
    weigh = models.IntegerField(default=0)
    status = models.CharField(max_length=10, default='temp')        # url


class AnticipateArchive(models.Model):
    """
    List of anticipated posts
    """
    id = models.CharField(max_length=50, primary_key=True)
    group = models.ForeignKey(Group, related_name='antiArchives')
    user = models.ForeignKey(FBUser, related_name='antiArchives')
    message = models.TextField(null=True, blank=True)
    time = models.DateTimeField()
    status = models.CharField(max_length=10, default='temp')


class AnalysisDBSchema(models.Model):
    """
    average data of groups
    """
    group = models.ForeignKey(Group, related_name='analysisSchema')
    avgpostlike = models.IntegerField(default=0)
    avgpostcomment = models.IntegerField(default=0)
    avgcomtlike = models.IntegerField(default=0)
    avgcomtcomment = models.IntegerField(default=0)
    lastupdatetime = models.DateTimeField()
    
    
class UpdateList(models.Model):
    """
    Update list for check analysis is update
    """
    method = models.CharField(max_length=30)
    updated_time = models.DateTimeField(auto_now_add=True)
    data = models.TextField(blank=True, null=True)

    @classmethod
    def update(cls, method, data=None):
        """
        Update list

        :param method: method
        :param data: data
        :return:
        """
        oj = UpdateList.objects.filter(method=method)
        if oj:
            oj[0].updated_time = timezone.now()
            oj[0].data = data
            oj[0].save()
        else:
            oj = UpdateList(method=method)
            oj.save()

    def is_update(self):
            """
            Check update is possible. (per 1 day)

            :return:
            """
            now = timezone.now()
            diff = now - self.updated_time

            if diff.days >= 1:
                return True
            return False


class GroupDurations(models.Model):
    """
    Total years and months from creation of group to now
    """
    group = models.ForeignKey(Group)
    yeared = models.IntegerField(default=0)
    monthed = models.IntegerField(default=0)
    lastupdatetime = models.DateTimeField()
    oldtimed = models.DateTimeField()


class MonthlyWords(models.Model):
    """
    Memoization about month words
    """
    group = models.ForeignKey(Group)
    word = models.CharField(max_length=255)
    weigh = models.IntegerField(default=0)
    lastfeeddate = models.DateTimeField()


class WeeklyWords(models.Model):
    """
    Memoization about week words
    """
    group = models.ForeignKey(Group)
    word = models.CharField(max_length=255)
    weigh = models.IntegerField(default=0)
    lastfeeddate = models.DateTimeField()


class WordsDiction(models.Model):
    """
    Temporary words for calculating
    """
    group = models.ForeignKey(Group)
    word = models.CharField(max_length=255)
    count = models.IntegerField(default=0)


class MonthTrendWord(models.Model):
    """
    Trend words on every month
    """
    datedtime = models.DateTimeField()
    group = models.ForeignKey(Group)
    word = models.CharField(max_length=255)
    weigh = models.IntegerField(default=1)
    lastfeeddate = models.DateTimeField()
