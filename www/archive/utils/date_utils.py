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
""" Provides date utils """

from django.utils import timezone
import datetime

__author__ = "Donghyun Seo"
__copyright__ = "Copyright ⓒ 2015, All rights reserved."
__email__ = "egaoneko@naver.com"


def week_range(date):
    """
    Find the first/last day of the week for the given day.
    Assuming weeks start on Sunday and end on Saturday.

    :param date: given day
    :return: a tuple of (from_date, to_date)
    """
    # isocalendar calculates the year, week of the year, and day of the week.
    # dow is Mon = 1, Sat = 6, Sun = 7
    year, week, dow = date.isocalendar()

    # Find the first day of the week.
    if dow == 7:
        # Since we want to start with Sunday, let's test for that condition.
        from_date = date
    else:
        # Otherwise, subtract `dow` number days to get the first day
        todate = date - timezone.timedelta(dow)

    # Now, add 6 for the last day of the week (i.e., count up to Saturday)
    to_date = from_date + timezone.timedelta(6)

    return from_date, to_date


def week_delta():
    """
    Find the first/last day of the week for today.
    Assuming weeks from last week day to current day.

    :return: a tuple of (from_date, to_date)
    """
    return timezone.now() - timezone.timedelta(days=7), timezone.now()


def date_range(date, days):
    """
    Return date after given days

    :param date: origin date
    :param days: after days
    :return: a tuple of (from_date, to_date)
    """
    return date, date + timezone.timedelta(days=days)


def get_date_from_str(str):
    """
    Retrun date from string

    :param str: string
    :return:
    """
    return timezone.datetime.strptime(str, '%Y-%m-%d').date()


def get_today():
    """
    Return today

    :return: today
    """
    return timezone.datetime.today()


def combine_min_time(date):
    """
    Combine `date` with min time value (00:00)

    :param date: date
    :return: date combined min time
    """
    return timezone.datetime.combine(date, datetime.time.min).replace(tzinfo=timezone.utc)


def combine_max_time(date):
    """
    Combine `date` with max time value (23:59:99)

    :param date: date
    :return: date combined max time
    """
    return timezone.datetime.combine(date, datetime.time.max).replace(tzinfo=timezone.utc)


def combine_time_2day(from_date, to_date):
    """
    Return combine time

    :param from_date: from date
    :param to_date: to date
    :return: (from_date, to_date)
    """
    # combine `from_date` with min time value (00:00)
    from_date = combine_min_time(from_date)
    # combine `to_date` with max time value (23:59:99) to have end date
    to_date = combine_max_time(to_date)
    return from_date, to_date
