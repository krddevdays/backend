from django.contrib.postgres.fields import JSONField
from django.db import models

from events.models import Event


class Order(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    email = models.EmailField()
    full_name = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.id} ({self.email})'


class Ticket(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    email = models.EmailField()
    full_name = models.CharField(max_length=150)
    form = JSONField(default=dict)

    class Meta:
        unique_together = ('order', 'email')

    def __str__(self):
        return f'Order {self.order_id}/{self.email}'
