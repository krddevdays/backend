import dateutil.parser
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event, Activity
from .qtickets import QTicketsInfo, TicketsSerializer
from .serializers import EventSerializer, ActivitySerializer, QTicketsOrderSerializer


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
        event = self.get_object()
        if event.external_id is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            event_data = QTicketsInfo.get_event_data(event.external_id)
            seats_data = QTicketsInfo.get_seats_data(event_data['shows'][0]['id'])
            tickets = TicketsSerializer(data={'event_data': event_data, 'seats_data': seats_data})

            tickets.is_valid(raise_exception=True)
            return Response(data=tickets.data)

    @action(methods=['POST'], detail=True, serializer_class=QTicketsOrderSerializer)
    def order(self, *args, **kwargs):
        event = self.get_object()
        if event.external_id is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            event_info = QTicketsInfo.get_event_data(event.external_id)
            seats = QTicketsInfo.get_seats_data(select_fields=["free_quantity", "disabled"], show_id=event_info['shows'][0]['id'])
        except Exception:
            return Response(status=502)

        order = self.get_serializer(data=self.request.data)
        order.is_valid(raise_exception=True)
        data = order.data

        current_show = event_info['shows'][0]
        if (
                not event_info['is_active']
                or not current_show['is_active']
                or current_show['sale_start_date'] is None
                or dateutil.parser.parse(current_show['sale_start_date']) > timezone.now()
                or dateutil.parser.parse(current_show['sale_finish_date']) < timezone.now()
                or data['payment_id'] not in [p['id'] for p in event_info['payments']]
        ):
            return Response(data={'error': 'Неверные данные для зказа'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={})


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
