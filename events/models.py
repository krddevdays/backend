from django.db import models
from django_enumfield import enum


class ActivityType(enum.Enum):
    WELCOME = 0
    TALK = 1
    COFFEE = 2
    LUNCH = 3


class Event(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Activity(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    type = enum.EnumField(ActivityType)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Activities'

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
