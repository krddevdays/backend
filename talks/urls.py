from django.urls import include, path
from rest_framework import routers

from talks.views import TalkViewSet

router = routers.DefaultRouter()
router.register(r'talks', TalkViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
