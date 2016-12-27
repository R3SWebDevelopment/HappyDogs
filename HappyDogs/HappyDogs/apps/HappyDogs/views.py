from HappyDogs.lib.decorators import render
from HappyDogs.lib.utils import get_request_data
from django.views.decorators.http import require_http_methods
from models import BoardingVisit, Dog
from datetime import date
from django.db.models import Avg, Max, Min
from utils import weeks_beetwen
from utils import parse_date
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt



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

@happy_dogs(template="dogs.html", content_type="html")
def happy_dogs_create_dogs(request):
    url = reverse('happy_dogs_create_dog_visits')
    Dog.generate_random_dog()
    return{
        'redirect' : True,
        'url' : url,
    }

@happy_dogs(template="dogs.html", content_type="html")
def happy_dogs_create_dog_visits(request):
    buck_size = 10
    url = reverse('happy_dogs_create_dog_visits')
    index = request.GET.get('index') or 0
    data = Dog.objects.all()
    try:
        index = int(index)
    except:
        index = data.count()
    if index < data.count():
        if index + buck_size < data.count():
            end = index + buck_size
        else:
            end = data.count() - 1
        dogs = data[index:end]
        for dog in dogs:
            dog.generate_random_visit
        index = end
    index += 1
    if index < data.count():
        url = "{}?index={}".format(url, index)
    else:
        url = reverse('happy_dogs_home')
    return{
        'redirect' : True,
        'url' : url,
    }

@happy_dogs(template="dogs.html", content_type="html")
def happy_dogs_create_data(request):
    url = reverse('happy_dogs_create_dogs')
    Dog.clear()
    BoardingVisit.clear()
    return{
        'redirect' : True,
        'url' : url,
    }

@csrf_exempt
@happy_dogs(template="", content_type="json")
def happy_dogs_rest_add_dogs_visit(request):
    error_message = ""
    added = False
    start_date = request.GET.get('start_date') or None
    if start_date is not None and start_date.strip():
        start_date = "{}".format(start_date)
    end_date = request.GET.get('end_date') or None
    if end_date is not None and end_date.strip():
        end_date = "{}".format(end_date)
    uuid = request.GET.get('uuid') or None
    if uuid is not None and uuid.strip():
        dog = Dog.objects.filter(uuid = uuid).first()
        if dog is not None:
            try:
                visit, added = dog.add_visit(start_date=start_date, end_date=end_date)
                saved = True
            except Exception, e:
                error_message = "{}".format(e)
        else:
            error_message = "Dog not selected"
    else:
        error_message = "Dog not selected"
    data = {
        'added' : added,
        'error_message' : error_message,
    }
    response_data = {
        'dog' : data,
    }
    return{
        'response_data' : response_data,
    }

@csrf_exempt
@happy_dogs(template="", content_type="json")
def happy_dogs_rest_detail(request):
    detail = []
    requested_date = request.GET.get('date') or None
    if requested_date is not None:
        requested_date = parse_date(input_date = requested_date)
    if requested_date is not None:
        data = BoardingVisit.date_visits(date_obj=requested_date)
        for d in data:
            detail.append({
                'dog_name' : d.dog_name,
                'dog_url' : d.dog_url,
                'start_date' : d.start_date.strftime('%m/%d/%Y'),
                'end_date' : d.end_date.strftime('%m/%d/%Y'),
            })
    response_data = {
        'detail' : detail
    }
    return{
        'response_data' : response_data,
    }

@csrf_exempt
@happy_dogs(template="", content_type="json")
def happy_dogs_rest_dogs(request):
    data = []
    dogs = Dog.objects.all()
    for d in dogs:
        data.append({
            'full_name' : d.full_name,
            'url' : d.url,
            'uuid' : d.uuid,
            'visits' : d.visits,
            'in_house' : d.is_the_house(),
            'in_house_label': d.is_the_house_label(),
        })
    response_data = {
        'dogs' : data,
    }
    return{
        'response_data' : response_data,
    }

@csrf_exempt
@happy_dogs(template="", content_type="json")
def happy_dogs_rest_dog(request):
    data = {}
    uuid = request.GET.get('uuid') or None
    if uuid is not None:
        dog = Dog.objects.filter(uuid = uuid).first()
        if dog is not None:
            data = {
                'full_name' : dog.full_name,
                'first_name' : dog.first_name,
                'last_name' : dog.last_name,
                'url' : dog.url,
                'uuid' : dog.uuid,
                'visits' : dog.visits_detail,
                'in_house' : dog.is_the_house(),
                'in_house_label': dog.is_the_house_label(),
            }
    response_data = {
        'dog' : data,
    }
    return{
        'response_data' : response_data,
    }

@csrf_exempt
@happy_dogs(template="", content_type="json")
def happy_dogs_rest_add_dog(request):
    error_message = ""
    added = False
    first_name = request.GET.get('first_name') or None
    last_name = request.GET.get('last_name') or None
    if first_name is not None and first_name.strip():
        try:
            dog, added = Dog.add(first_name=first_name , last_name=last_name)
            saved = True
        except Exception, e:
            error_message = "{}".format(e)
    data = {
        'added' : added,
        'error_message' : error_message,
    }
    response_data = {
        'dog' : data,
    }
    return{
        'response_data' : response_data,
    }

@csrf_exempt
@happy_dogs(template="", content_type="json")
def happy_dogs_rest_update_dog(request):
    data = {}
    uuid = request.GET.get('uuid') or None
    first_name = request.GET.get('first_name') or None
    last_name = request.GET.get('last_name') or None
    error_message = ""
    saved = False
    if uuid is not None:
        dog = Dog.objects.filter(uuid = uuid).first()
        if first_name is not None and first_name.strip():
            try:
                dog = dog.update(first_name = first_name , last_name = last_name)
                saved = True
            except Exception,e:
                error_message = "{}".format(e)
        if dog is not None:
            data = {
                'full_name' : dog.full_name,
                'first_name' : dog.first_name,
                'last_name' : dog.last_name,
                'url' : dog.url,
                'uuid' : dog.uuid,
                'visits' : dog.visits_detail,
                'in_house' : dog.is_the_house(),
                'in_house_label': dog.is_the_house_label(),
                'saved' : saved,
                'error_message' : error_message,
            }
    response_data = {
        'dog' : data,
    }
    return{
        'response_data' : response_data,
    }

@csrf_exempt
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