from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateTimeFilter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .interfaces import PartnerType, EventStatusType
from .models import Event, Activity
from .qtickets import QTicketsInfo, TicketsSerializer
from .serializers import EventSerializer, ActivitySerializer, QTicketsOrderSerializer, PartnerSerializer


class EventFilter(FilterSet):
    date_from = DateTimeFilter(field_name="start_date", lookup_expr='gt')
    date_to = DateTimeFilter(field_name="start_date", lookup_expr='lt')

    class Meta:
        model = Event
        fields = ('date_from', 'date_to')


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.order_by('-start_date')
    serializer_class = EventSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = EventFilter
    search_fields = ('name',)

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and (user.is_staff or user.has_perm('events.view_draft')):
            return qs.all()
        return qs.exclude(status=EventStatusType.DRAFT)

    @action(detail=True)
    def activities(self, *args, **kwargs):
        event = self.get_object()
        serializer = ActivitySerializer(event.activities.all(), many=True)
        return Response(serializer.data)

    @action(detail=True)
    def partners(self, *args, **kwargs):
        event = self.get_object()
        qs = event.partners.order_by('order').all()
        result = {category: PartnerSerializer(qs.filter(type=type_id), many=True).data
                  for category, type_id in PartnerType.items()}
        return Response(result)

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

        order = self.get_serializer(event_id=event.external_id, data=self.request.data)
        order.is_valid(raise_exception=True)

        try:
            qticket_response = order.order_tickets(
                host=self.request.META.get('HTTP_HOST', 'krd.dev'),
                external_id=event.external_id
            )
            required_fields = ('cancel_url', 'payment_url', 'price', 'currency_id', 'reserved_to', 'id')
            response = {key: value for key, value in qticket_response.items() if key in required_fields}
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse(response)


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
