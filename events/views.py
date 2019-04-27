from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event, Activity
from .serializers import EventSerializer, ActivitySerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=True)
    def activities(self, *args, **kwargs):
        event = self.get_object()
        serializer = ActivitySerializer(event.activities.all(), many=True)
        return Response(serializer.data)

    @action(detail=True)
    def tickets(self, *args, **kwargs):
        return Response(data={})


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
