from django.db import models
from django_enumfield import enum

from events.interfaces import ActivityType, WelcomeActivity, CoffeeActivity, LunchActivity
from .qtickets import check_qtickets_event


class Venue(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f'{self.name}, {self.address}'


class Zone(models.Model):
    name = models.CharField(max_length=50)
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name='zone')

    def __str__(self):
        return f'{self.name} ({self.venue.name})'


class Event(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT)
    external_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}, {self.start_date:%d.%m.%Y}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.external_id is not None:
            check_qtickets_event(self.external_id)
        super(Event, self).save(force_insert, force_update, using, update_fields)


class Activity(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='activities')
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)
    type = enum.EnumField(ActivityType)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f'{self.event} - {self.zone} - {self.start_date:%d.%m.%Y-%H:%M}'

    @property
    def thing(self):
        items = {
            ActivityType.TALK: getattr(self, 'talk', None),
            ActivityType.WELCOME: WelcomeActivity(),
            ActivityType.COFFEE: CoffeeActivity(),
            ActivityType.LUNCH: LunchActivity(),
        }
        return items.get(self.type)
