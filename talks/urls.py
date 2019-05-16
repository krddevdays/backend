from django.urls import include, path
from rest_framework import routers

from talks.views import TalkViewSet, DiscussionViewSet

router = routers.DefaultRouter()
router.register(r'talks', TalkViewSet)
router.register(r'discussions', DiscussionViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
