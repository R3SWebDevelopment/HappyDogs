from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'home_calendar.json$' , happy_dogs_rest_visits, name='happy_dogs_rest_visits'),
]