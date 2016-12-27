from datetime import date
from dateutil import rrule
import datetime
from datetime import timedelta

INPUT_DATE_FORMAT = '%m/%d/%Y'

def parse_date(input_date=None):
    date_obj = None
    if input_date is not None and (input_date.__class__ is str or input_date.__class__ is unicode):
        try:
            date_obj = datetime.datetime.strptime(input_date, INPUT_DATE_FORMAT)
            date_obj.date()
        except:
            pass
    return date_obj


def weeks_beetwen(start_date=None, end_date=None , filtered=False):
    weeks = 0
    days = 0
    starting_date = None
    ending_date = None
    daysList = []
    if start_date is not None and end_date is not None and start_date < end_date:
        if start_date.isoweekday() == 1:
            starting_date = start_date
        else:
            to_start = start_date.isoweekday() - 1
            starting_date = start_date - datetime.timedelta(days=to_start)
        if end_date.isoweekday() == 7:
            ending_date = end_date
        else:
            to_end = 7 - end_date.isoweekday()
            ending_date = end_date + datetime.timedelta(days=to_end)

        weeks_ruled = rrule.rrule(rrule.WEEKLY, dtstart=starting_date, until=ending_date)
        days_ruled = rrule.rrule(rrule.DAILY, dtstart=starting_date, until=ending_date)
        weeks = weeks_ruled.count()
        days = days_ruled.count()
        daysList = list(days_ruled)
    return weeks, days , starting_date, ending_date , daysList


def generate_weekend_list_of_range(start_date = None , end_date = None):
    date_list = []
    start_date = parse_date(input_date=start_date)
    end_date = parse_date(input_date=end_date)
    if start_date is not None and end_date is not None:
        delta = timedelta(days=1)
        d = start_date
        weekend = set([4, 5])
        while d <= end_date:
            if d.weekday() in weekend:
                date_list.append(d.date())
            d += delta
    return date_list

def generate_day_list_of_range(start_date = None , end_date = None):
    date_list = []
    start_date = parse_date(input_date=start_date)
    end_date = parse_date(input_date=end_date)
    if start_date is not None and end_date is not None:
        delta = timedelta(days=1)
        d = start_date
        while d <= end_date:
            date_list.append(d.date())
            d += delta
    return date_list

def generate_holidays_list():
    date_list = []
    delta = timedelta(days=2)
    holidays = [
        '1/1/2016',
        '1/18/2016',
        '2/15/2016',
        '5/30/2016',
        '7/4/2016/',
        '9/5/2016',
        '10/10/2016',
        '11/11/2016',
        '11/24/2016',
        '12/25/2016',
        '12/26/2016',
    ]
    for hd in holidays:
        date_obj = parse_date(input_date=hd)
        if date_obj is not None:
            before = date_obj - delta
            after = date_obj + delta
            date_list.append(before.date())
            date_list.append(after.date())
    return date_list