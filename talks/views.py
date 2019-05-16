from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import viewsets

from talks.models import Talk
from .serializers import TalkSerializer


class TalkFilter(FilterSet):
    class Meta:
        model = Talk
        fields = ('event_id', )


class TalkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Talk.objects.all()
    serializer_class = TalkSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TalkFilter
