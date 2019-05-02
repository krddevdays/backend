from collections import Counter

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
                not event_info['is_active']  # эвент должен быть активен
                or not current_show['is_active']  # show должно быть активным
                or
                (
                        current_show['sale_start_date'] is not None
                        and dateutil.parser.parse(current_show['sale_start_date']) >= timezone.now()
                )
                or dateutil.parser.parse(current_show['sale_finish_date']) < timezone.now()
                or data['payment_id'] not in [p['id'] for p in event_info['payments']]
        ):
            return Response(data={'error': 'Неверные данные для зказа'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            payment = [p for p in event_info['payments'] if p['id'] == data['payment_id']][0]
        except IndexError:
            return Response(data={'error': 'Неверный id платежа'})
        if payment['handler'] == 'invoice' and {'inn', 'legal_name'} - set(data):
            return Response(data={'error': 'Неверные данные для зказа, ИНН и наименование организации не указанны'},
                            status=status.HTTP_400_BAD_REQUEST)

        # email должны быть уникальны в рамках tickets из данного запроса
        tickets_emails = [ticket['email'] for ticket in data['tickets']]
        if len(tickets_emails) > len(set(tickets_emails)):
            return Response(data={'error': 'Адреса электронной почты не уникальны'})

        seats_by_type = Counter([el['type_id'] for el in data['tickets']])

        for ticket_request in data['tickets']:
            if (
                    ticket_request['type_id'] not in seats
                    or [i for i in seats[ticket_request['type_id']]['seats'].values()][0]['disabled']
                    or seats_by_type[ticket_request['type_id']] >
                    [i for i in seats[ticket_request['type_id']]['seats'].values()][0]['free_quantity']
                    # fixme: проверка проходит много раз, а должна быть одна и сразу
            ):
                return Response(data={'error': 'Неверные данные для зказа'}, status=status.HTTP_400_BAD_REQUEST)

        order_body = {
            'email': data['email'],
            'name': data['first_name'],
            'surname': data['last_name'],
            'phone': data.get('phone', ''),
            'host': self.request.META['HTTP_HOST'],
            'payment_id': data['payment_id'],
            'event_id': event.external_id,
            'baskets': [
                {
                    'show_id': current_show['id'],
                    'seat_id': basket['type_id'],
                    'client_email': basket['email'],
                    'client_name': basket['first_name'],
                    'client_surname': basket['last_name']

                }
                for basket
                in data['tickets']
            ]
        }
        juridicial = False
        if 'inn' in data:
            order_body.update({'legal_name': data['legal_name'], 'inn': data['inn']})
            juridicial = True

        try:
            payment_url = QTicketsInfo.get_order_tickets_url(tickets_data=order_body, juridicial=juridicial)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data={'url': payment_url})


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
