from django.conf.urls import include, url
from HappyDogs.apps.HappyDogs.views import happy_dogs_home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', happy_dogs_home , name='index'),
    url(r'^happy_dogs/', include('HappyDogs.apps.HappyDogs.urls')),
    url(r'^rest/happy_dogs/', include('HappyDogs.apps.HappyDogs.rest_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
