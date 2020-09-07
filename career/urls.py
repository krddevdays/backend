from django.urls import include, path
from rest_framework import routers

from .views import VacancyViewSet

router = routers.DefaultRouter()
router.register(r'vacancy', VacancyViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
