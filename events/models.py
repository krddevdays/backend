from django.db import models
from django_enumfield import enum


class ActivityType(enum.Enum):
    WELCOME = 0
    TALK = 1
    COFFEE = 2
    LUNCH = 3


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
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name}, {self.start_date:%d.%m.%Y}'


class Activity(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='activities')
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)
    type = enum.EnumField(ActivityType)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Activities'

    def __str__(self):
        return self.name
