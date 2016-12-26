from HappyDogs.lib.decorators import render
from HappyDogs.lib.utils import get_request_data
from django.views.decorators.http import require_http_methods
from models import BoardingVisit, Dog
from datetime import date
from django.db.models import Avg, Max, Min
from utils import weeks_beetwen
from utils import parse_date



def happy_dogs(template=None, content_type=None, **kwargs):
    path = 'happy_dogs'
    template = "%s/%s" % (path, template)
    return render(path=template, content_type=content_type, **kwargs)


@happy_dogs(template="home.html", content_type="html")
def happy_dogs_home(request):
    return {
    }

@happy_dogs(template="dog.html", content_type="html")
def happy_dogs_dogs(request):
    return {
    }

@happy_dogs(template="dogs.html", content_type="html")
def happy_dogs_dog(request, dog_uuid=None):
    return {
    }

@happy_dogs(template="", content_type="json")
def happy_dogs_rest_visits(request):
    weeks = []
    start_date = request.GET.get('start_date') or None
    if start_date is not None:
        start_date = parse_date(input_date = start_date)
    end_date = request.GET.get('end_date') or None
    if end_date is not None:
        end_date = parse_date(input_date = end_date)
    visits = BoardingVisit.visits(start_date=start_date, end_date=end_date)
    daysList = []
    if visits is not None and visits.exists():
        today = date.today()
        max_min = visits.aggregate(Max('start_date'), Min('start_date'), Max('end_date'), Min('end_date'))
        min_date = None
        max_date = None
        range = None
        if max_min is not None:
            end_date__max = max_min.get('end_date__max') or None
            end_date__min = max_min.get('end_date__min') or None
            start_date__max = max_min.get('start_date__max') or None
            start_date__min = max_min.get('start_date__min') or None
            if end_date__min is not None and start_date__min is not None:
                if end_date__min < start_date__min:
                    min_date = end_date__min
                else:
                    min_date = start_date__min
            elif end_date__min is not None:
                min_date = end_date__min
            elif start_date__min is not None:
                min_date = start_date__min
            else:
                min_date = today
            if end_date__max is not None and start_date__max is not None:
                if end_date__max > start_date__max:
                    max_date = end_date__max
                else:
                    max_date = start_date__max
            elif end_date__max is not None:
                max_date = end_date__max
            elif start_date__max is not None:
                max_date = start_date__max
            else:
                max_date = today
        if end_date is not None and start_date is not None:
            weeks_count, days_count, starting_date, ending_date, daysList = weeks_beetwen(start_date=start_date, end_date=end_date, filtered=True)
        else:
            weeks_count, days_count, starting_date, ending_date, daysList = weeks_beetwen(start_date=min_date, end_date=max_date)
    day_index = 1
    week_data = []
    week_counter = 1
    for day in daysList:
        dogs_in_house = BoardingVisit.dogs_in_house(date_obj=day.date())
        week_data.append({
            'dogs_in_house' : dogs_in_house,
            'date' : day.strftime('%m/%d/%Y') ,
            'weekday' : day.isoweekday(),
            'small_date' : day.strftime('%b %d') ,
            'week' : week_counter,
        })
        day_index += 1
        if day_index > 7:
            day_index
            weeks.append(week_data)
            week_data = []
            day_index = 1
            week_counter += 1
    response_data = {
        'weeks' : weeks,
    }
    return {
        'response_data' : response_data
    }

@happy_dogs(template="", content_type="json")
def happy_dogs_rest_visit(request):
    return {
    }

@happy_dogs(template="", content_type="json")
def happy_dogs_est_add_visit(request):
    return {
    }

@happy_dogs(template="", content_type="json")
def happy_dogs_rest_dogs(request):
    return {
    }

@happy_dogs(template="", content_type="json")
def happy_dogs_rest_add_dog(request):
    return {
    }

@happy_dogs(template="", content_type="json")
def happy_dogs_rest_edit_dog(request):
    return {
    }

