"""
A colleciton of useful tools for date/time related.

When we are considering a period between two dates, the period would
include both start date and end date(it is [s, e], not [s, e)).
"""

from dateutil import rrule, easter
import datetime
import time


def weeks_between(start_date, end_date):
    """Return how many weeks between start_date and end_date.

    example:
    >>> import datetime
    >>> start_date = datetime.date(2000, 1, 1)
    >>> end_date = datetime.date(2000,1 , 15)
    >>> weeks_between(start_date, end_date)
    3
    """
    weeks = rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)
    return weeks.count()


def workdays(start, end, holidays=0, days_off=None):
    """Returns the work days between two dates.

    example:
    >>> import datetime
    >>> s = datetime.date(2000, 1, 1)
    >>> e = datetime.date(2000, 1, 15)
    >>> workdays(s, e, 2)
    8
    """
    if days_off is None:
        days_off = 5, 6     # sat. and sun.
    wdays = [x for x in range(7) if x not in days_off]
    days = rrule.rrule(rrule.DAILY, dtstart=start,
                       until=end, byweekday=wdays)
    return days.count() - holidays


def all_easter(start, end):
    """Returns all the Easter days between start and end.

    example:
    >>> import datetime
    >>> from datetime import date
    >>> all_easter(date(2012, 1, 1), date(2013, 12, 30))
    [datetime.date(2012, 4, 8), datetime.date(2013, 3, 31)]
    """
    easters = [easter.easter(year) for year in
               xrange(start.year, end.year+1)]
    return [d for d in easters if start <= d <= end]


def all_boxing(start, end):
    """Returns all boxing days between start and end.

    example:
    >>> import datetime
    >>> from datetime import date
    >>> all_boxing(date(2012, 1, 1), date(2013, 12, 30))
    [datetime.date(2012, 4, 9), datetime.date(2013, 4, 1)]
    """
    one_day = datetime.timedelta(days=1)
    boxings = [easter.easter(year)+one_day for year in
               xrange(start.year, end.year+1)]
    return [d for d in boxings if start <= d <= end]


def all_christmas(start, end):
    """Returns all christmas days between start and end.

    example:
    >>> import datetime
    >>> from datetime import date
    >>> all_christmas(date(2012, 1, 1), date(2013, 12, 30))
    [datetime.date(2012, 12, 25), datetime.date(2013, 12, 25)]
    """
    christmas = [datetime.date(year, 12, 25) for year in
                 xrange(start.year, end.year+1)]
    return [d for d in christmas if start <= d <= end]


def is_dst():
    """Check if it is DST time"""
    return bool(time.localtime().tm_isdst)
