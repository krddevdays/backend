from django.urls import include, path
from rest_framework import routers

from .views import VacancyViewSet, SkillViewSet

router = routers.DefaultRouter()
router.register(r'vacancies', VacancyViewSet)
router.register(r'skills', SkillViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
