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
from django.utils import timezone

from archive.models import Group


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
