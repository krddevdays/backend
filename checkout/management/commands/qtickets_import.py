from django.core.management import BaseCommand

from checkout.models import Order, Ticket
from events.models import Event
from events.qtickets import QTicketsInfo


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        event = Event.objects.get(pk=1)
        qtickets = QTicketsInfo.get_order_list(event.external_id)
        for item in qtickets:
            client = item['client']
            tickets = item['baskets']
            order = Order.objects.create(
                event=event, response=item, email=client['email'], first_name=client['details']['name'],
                last_name=client['details']['surname'])
            for ticket in tickets:
                Ticket.objects.create(
                    order=order, email=ticket['client_email'], qticket_id=ticket['id'],
                    first_name=ticket['client_name'], last_name=ticket['client_surname'])
