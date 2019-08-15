from django.core.management import BaseCommand

from checkout.models import Order
from events.models import Event
from events.qtickets import QTicketsInfo


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('event_ids', nargs='+', type=int)

    def handle(self, *args, **kwargs):
        for event_id in kwargs['event_ids']:
            event = Event.objects.get(pk=event_id)
            print(f'Process event {event.name}')
            qtickets = QTicketsInfo.get_order_list(event.external_id)
            for item in qtickets:
                Order.add_or_update(item)
