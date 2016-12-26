from django.conf.urls import include, url
urlpatterns = [
    url(r'^happy_dogs/', include('HappyDogs.apps.HappyDogs.urls')),
    url(r'^rest/happy_dogs/', include('HappyDogs.apps.HappyDogs.rest_urls')),
]
