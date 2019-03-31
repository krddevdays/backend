from django.urls import include, path
from rest_framework import routers

from events.views import EventViewSet

router = routers.DefaultRouter()
router.register(r'events', EventViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
