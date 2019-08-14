from django.contrib.postgres.fields import JSONField
from django.db import models

from events.models import Event
from users.models import User


class ContactsMixin(models.Model):
    email = models.EmailField(db_index=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        abstract = True


class Order(ContactsMixin, models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    response = JSONField(default=dict)
    qticket_id = models.PositiveIntegerField(db_index=True)

    def __str__(self):
        return f'{self.id} ({self.email})'

    @classmethod
    def add(cls, item):
        event = Event.objects.get(external_id=item['event_id'])
        client = item['client']
        tickets = item['baskets']
        order = Order.objects.create(
            event=event, response=item, email=client['email'], qticket_id=item['id'],
            first_name=client['details']['name'], last_name=client['details']['surname'])
        for ticket in tickets:
            Ticket.objects.create(
                order=order, email=ticket['client_email'], qticket_id=ticket['id'],
                first_name=ticket['client_name'], last_name=ticket['client_surname'])


class Ticket(ContactsMixin, models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    qticket_id = models.PositiveIntegerField(db_index=True)

    def __str__(self):
        return f'Order {self.order_id}/{self.email}'
