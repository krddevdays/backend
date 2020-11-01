from rest_framework import viewsets, mixins, permissions

from krddevdays.pagination import PagePagination
from .models import Vacancy, Skill
from .serializers import VacancySerializer, SkillSerializer


class VacancyViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                     mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Vacancy.objects.order_by('-created_at').all()
    serializer_class = VacancySerializer
    pagination_class = PagePagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer: VacancySerializer):
        serializer.save(user=self.request.user)


class SkillViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
