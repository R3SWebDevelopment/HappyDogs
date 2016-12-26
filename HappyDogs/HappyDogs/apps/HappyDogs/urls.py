from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'$' , happy_dogs_home, name='happy_dogs_home'),
    url(r'dogs/$' , happy_dogs_dogs, name='happy_dogs_dogs'),
    url(r'dogs/(?P<uuid>\w+)/$' , happy_dogs_dog, name='happy_dogs_dog'),
]