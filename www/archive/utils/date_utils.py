from django.utils.timezone import now, datetime, timedelta

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
        todate = date - timedelta(dow)

    # Now, add 6 for the last day of the week (i.e., count up to Saturday)
    to_date = from_date + timedelta(6)

    return from_date, to_date


def week_delta():
    """
    Find the first/last day of the week for today.
    Assuming weeks from last week day to current day.

    :return: a tuple of (from_date, to_date)
    """
    return now() - timedelta(days=7), now()


def date_range(date, days):
    """
    Return date after given days

    :param date: origin date
    :param days: after days
    :return: a tuple of (from_date, to_date)
    """
    return date, date + timedelta(days=days)


def get_date_from_str(str):
    """
    Retrun date from string

    :param str: string
    :return:
    """
    return datetime.strptime(str, '%Y-%m-%d').date()


def get_today():
    """
    Return today

    :return: today
    """
    return datetime.today()
