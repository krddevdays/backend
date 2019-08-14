from django.core.management import BaseCommand

from checkout.models import Order
from events.models import Event
from events.qtickets import QTicketsInfo


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        event = Event.objects.get(pk=1)
        qtickets = QTicketsInfo.get_order_list(event.external_id)
        for item in qtickets:
            Order.add(item)
