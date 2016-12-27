from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'home_calendar.json$' , happy_dogs_rest_visits, name='happy_dogs_rest_visits'),
    url(r'detail_calendar.json$' , happy_dogs_rest_detail, name='happy_dogs_rest_detail'),
    url(r'dogs.json$' , happy_dogs_rest_dogs, name='happy_dogs_rest_dogs'),
    url(r'add_dog_visit.json$' , happy_dogs_rest_add_dogs_visit, name='happy_dogs_rest_add_dogs_visit'),

    url(r'update_dog.json$' , happy_dogs_rest_update_dog, name='happy_dogs_rest_update_dog'),
    url(r'add_dog.json$' , happy_dogs_rest_add_dog, name='happy_dogs_rest_add_dog'),
    url(r'dog.json$' , happy_dogs_rest_dog, name='happy_dogs_rest_dog'),
]