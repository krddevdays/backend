from rest_framework import viewsets, mixins, permissions

from .models import Vacancy, Technology
from .serializers import VacancySerializer, TechnologySerializer


class VacancyViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                     mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer: VacancySerializer):
        serializer.save(user=self.request.user)


class TechnologyViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
