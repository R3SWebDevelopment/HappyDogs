from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'create_data/$', happy_dogs_create_data, name='happy_dogs_create_data'),
    url(r'create_dogs/$', happy_dogs_create_dogs, name='happy_dogs_create_dogs'),
    url(r'create_dog_visits/$', happy_dogs_create_dog_visits, name='happy_dogs_create_dog_visits'),
    url(r'dogs/$', happy_dogs_dogs, name='happy_dogs_dogs'),
    url(r'$' , happy_dogs_home, name='happy_dogs_home'),
#    url(r'dogs/(?P<uuid>\w+)/$' , happy_dogs_dog, name='happy_dogs_dog'),
]