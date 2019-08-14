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

    def __str__(self):
        return f'{self.id} ({self.email})'


class Ticket(ContactsMixin, models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')
    form = JSONField(default=dict)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        unique_together = ('order', 'email')

    def __str__(self):
        return f'Order {self.order_id}/{self.email}'
