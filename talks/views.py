from django.http import HttpResponseBadRequest
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import viewsets, mixins, permissions
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

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


class DiscussionFilter(FilterSet):
    class Meta:
        model = Discussion
        fields = ('event_id', )


class DiscussionViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                        mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DiscussionFilter

    def perform_create(self, serializer: DiscussionSerializer):
        if (serializer.validated_data['event'].discussion_finish is not None) and \
           (timezone.now() > serializer.validated_data['event'].discussion_finish):
            raise ValidationError('Discussion submission closed')
        serializer.save(author=self.request.user)

    @detail_route(methods=('POST',))
    def vote(self, request, pk=None):
        instance: Discussion = self.get_object()
        if (instance.event.discussion_finish is not None) and (timezone.now() > instance.event.discussion_finish):
            return Response('Discussion vote closed', status=400)

        if request.user.id in instance.votes.values_list('id', flat=True):
            instance.votes.remove(request.user)
        else:
            instance.votes.add(request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
