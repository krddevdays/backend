from django import forms
from django.db import models
from django_enumfield import enum

from events.interfaces import ActivityType, WelcomeActivity, CoffeeActivity, LunchActivity, CloseActivity, PartnerType
from .qtickets import QTicketsInfo


class Venue(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f'{self.name}, {self.address}'


class Zone(models.Model):
    name = models.CharField(max_length=50)
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name='zones')
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.name} ({self.venue.name})'


class Event(models.Model):
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=500)
    full_description = models.TextField(null=True, blank=True)
    ticket_description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT)
    external_id = models.IntegerField(null=True, blank=True)
    image = models.URLField()
    image_vk = models.URLField(null=True, blank=True)
    image_facebook = models.URLField(null=True, blank=True)
    cfp_start = models.DateTimeField(null=True, blank=True)
    cfp_finish = models.DateTimeField(null=True, blank=True)
    cfp_url = models.URLField(null=True, blank=True)
    discussion_start = models.DateTimeField(null=True, blank=True)
    discussion_finish = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}, {self.start_date:%d.%m.%Y}'

    def clean(self):
        if self.external_id is not None:
            try:
                QTicketsInfo.check_event_exist(self.external_id)
            except Exception as e:
                raise forms.ValidationError({
                    'external_id': forms.ValidationError(str(e))
                })


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
            ActivityType.CLOSE: CloseActivity(),
            ActivityType.COFFEE: CoffeeActivity(),
            ActivityType.LUNCH: LunchActivity(),
        }
        return items.get(self.type)


class Partner(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='partners')
    type = enum.EnumField(PartnerType)
    name = models.CharField(max_length=100)
    image = models.URLField()
    link = models.URLField()
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name
