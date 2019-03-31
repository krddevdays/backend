from django.db import models
from django_enumfield import enum


class ActivityType(enum.Enum):
    WELCOME = 0
    TALK = 1
    COFFEE = 2
    LUNCH = 3


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Activity(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.PROTECT)
    type = enum.EnumField(ActivityType)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Activities'

    def __str__(self):
        return self.name
