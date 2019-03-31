from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from events.models import Event, Activity
from events.serializers import EventSerializer, ActivitySerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=True)
    def activities(self, *args, **kwargs):
        event = self.get_object()
        serializer = ActivitySerializer(event.activities.all(), many=True)
        return JsonResponse(serializer.data, safe=False)


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
