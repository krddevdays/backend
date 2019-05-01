from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateTimeFilter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .models import Event, Activity
from .qtickets import QTicketsInfo, TicketsSerializer
from .serializers import EventSerializer, ActivitySerializer


class EventFilter(FilterSet):
    date_from = DateTimeFilter(field_name="start_date", lookup_expr='gt')
    date_to = DateTimeFilter(field_name="start_date", lookup_expr='lt')

    class Meta:
        model = Event
        fields = ('date_from', 'date_to')


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.order_by('-start_date').all()
    serializer_class = EventSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = EventFilter
    search_fields = ('name',)

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
