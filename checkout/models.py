from django.db import models

from events.models import Event
from users.models import User


class ContactsMixin(models.Model):
    email = models.EmailField(db_index=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    client_phone = models.CharField(max_length=20, null=True, blank=True)
    qticket_id = models.PositiveIntegerField(db_index=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def _unpack(self, response, fields):
        for key, mapping in fields.items():
            obj = response
            try:
                while '.' in mapping:
                    path, mapping = mapping.split('.', 1)
                    obj = obj[path]
                else:
                    value = obj[mapping]
            except Exception:
                value = None
            setattr(self, key, value)


class Order(ContactsMixin, models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    response = models.JSONField(default=dict)
    payed_at = models.DateTimeField(null=True, blank=True)
    reserved_to = models.DateTimeField(null=True, blank=True)
    reserved = models.BooleanField(default=False, null=True)

    qticket_fields = {
        **{item: item for item in ('created_at', 'updated_at', 'deleted_at', 'payed_at', 'reserved_to',
                                   'reserved')},
        **{'client_phone': 'client.details.phone'}
    }

    def __str__(self):
        return f'{self.id} ({self.email})'

    @classmethod
    def add_or_update(cls, item):
        event = Event.objects.get(external_id=item['event_id'])
        client = item['client']
        try:
            order = Order.objects.get(qticket_id=item['id'])
        except Order.DoesNotExist:
            order = Order(event=event, qticket_id=item['id'])
        order.response = item
        order._unpack(item, Order.qticket_fields)
        order.email = client['email'].lower()
        if client['details']:
            order.first_name = client['details']['name']
            order.last_name = client['details']['surname']
        order.save()

        to_remove = set(order.tickets.values_list('qticket_id', flat=True))
        for ticket in item['baskets']:
            to_remove -= {ticket['id']}
            try:
                original = Ticket.objects.get(qticket_id=ticket['id'])
            except Ticket.DoesNotExist:
                original = Ticket(qticket_id=ticket['id'], order=order)
            email = ticket['client_email'].lower()
            if original.email != email:
                original.email = email
                original.user = None
            original._unpack(ticket, Ticket.qticket_fields)
            original.save()
        Ticket.objects.filter(qticket_id__in=list(to_remove)).delete()


class Ticket(ContactsMixin, models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='tickets')
    pdf_url = models.URLField(null=True, blank=True)
    passbook_url = models.URLField(null=True, blank=True)
    type = models.CharField(max_length=40, null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)

    qticket_fields = {
        **{
            'first_name': 'client_name',
            'last_name': 'client_surname',
            'type': 'seat_id',
        },
        **{item: item for item in ('created_at', 'updated_at', 'deleted_at', 'pdf_url', 'passbook_url',
                                   'price', 'refunded_at', 'client_phone')}
    }

    def __str__(self):
        return f'Order {self.order_id}/{self.email}'
