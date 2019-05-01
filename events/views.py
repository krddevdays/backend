from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event, Activity
from .qtickets import QTicketsInfo, TicketsSerializer
from .serializers import EventSerializer, ActivitySerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.order_by('-start_date').all()
    serializer_class = EventSerializer

    @action(detail=True)
    def activities(self, *args, **kwargs):
        event = self.get_object()
        serializer = ActivitySerializer(event.activities.all(), many=True)
        return Response(serializer.data)

    @action(detail=True)
    def tickets(self, *args, **kwargs):
        event = self.get_object()
        if event.external_id is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            event_data = QTicketsInfo.get_event_data(event.external_id)
            seats_data = QTicketsInfo.get_seats_data(event_data['shows'][0]['id'])
            tickets = TicketsSerializer(data={'event_data': event_data, 'seats_data': seats_data})

            tickets.is_valid(raise_exception=True)
            return Response(data=tickets.data)


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
