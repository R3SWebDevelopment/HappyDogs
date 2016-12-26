from datetime import date
from dateutil import rrule
import datetime

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

