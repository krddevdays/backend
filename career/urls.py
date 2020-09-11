from django.urls import include, path
from rest_framework import routers

from .views import VacancyViewSet, TechnologyViewSet

router = routers.DefaultRouter()
router.register(r'vacancy', VacancyViewSet)
router.register(r'technology', TechnologyViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
