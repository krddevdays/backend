from rest_framework import viewsets, mixins, permissions

from .models import Vacancy
from .serializers import VacancySerializer


class VacancyViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                     mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer: VacancySerializer):
        serializer.save(user=self.request.user)
