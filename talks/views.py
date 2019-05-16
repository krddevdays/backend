from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import viewsets, mixins, permissions

from talks.models import Talk, Discussion
from .serializers import TalkSerializer, DiscussionSerializer


class TalkFilter(FilterSet):
    class Meta:
        model = Talk
        fields = ('event_id', )


class TalkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Talk.objects.all()
    serializer_class = TalkSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TalkFilter


class DiscussionViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                        mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(speaker=self.request.user)
