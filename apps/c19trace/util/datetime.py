import pytz

from datetime import datetime, timedelta


def _start_date(tz=None, type=None):
    today = datetime.utcnow().replace(tzinfo=pytz.utc)
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)

    if tz:
        today = today.astimezone(pytz.timezone(tz))

    if type == 1:    # week
        substract_days = (today.weekday() + 1)
    elif type == 2:  # month
        substract_days = today.day

    if type:
        date = today - timedelta(days=substract_days)
    else:
        date = today

    if tz:
        date.astimezone(pytz.utc)

    return date.replace(tzinfo=None)


def start_day_date(tz=None):
    return _start_date(tz)


def start_week_date(tz=None):
    return _start_date(tz, 1)


def start_month_date(tz=None):
    return _start_date(tz, 2)