from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'home_calendar.json$' , happy_dogs_rest_visits, name='happy_dogs_rest_visits'),
    url(r'detail_calendar.json$' , happy_dogs_rest_detail, name='happy_dogs_rest_detail'),
]