from datetime import timedelta
from pytz import timezone, all_timezones


def get_timezones():
    """retrieve list of valid timezones"""
    return set(list(all_timezones) + ['PST', 'CST', 'EST', 'GMT'])


def get_time(tz, time):
    """helper function to map provided datetime(UTC) to timezone"""
    tzUpper = tz.upper()
    if tzUpper == 'PST':
        time -= timedelta(hours=8)
    elif tzUpper == 'CST':
        time -= timedelta(hours=6)
    elif tzUpper == 'EST':
        time -= timedelta(hours=5)
    elif tzUpper == 'GMT':
        time -= timedelta(hours=0)
    else:
        other_zone = timezone(tz)
        time = time.astimezone(other_zone)
    return time
