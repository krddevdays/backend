from django.utils import timezone
from factory import fuzzy, SubFactory, SelfAttribute, Iterator
from factory.django import DjangoModelFactory

from . import models


class LocationFactory(DjangoModelFactory):
    class Meta:
        model = models.Location

    name = Iterator(['London', 'CoPlace'])
    address = Iterator(['Backer street 221b', 'Krasnoarmeyskaya 55/1'])


class EventFactory(DjangoModelFactory):
    class Meta:
        model = models.Event

    name = fuzzy.FuzzyText(prefix='KrdDevDays ')  # just for fun
    start_date = fuzzy.FuzzyDateTime(start_dt=timezone.now())
    finish_date = fuzzy.FuzzyDateTime(start_dt=timezone.now())

    location = SubFactory(LocationFactory)


class PlaceFactory(DjangoModelFactory):
    class Meta:
        model = models.Place

    name = Iterator(['Big room', 'Conference room', 'Small room'])

    location = SubFactory(LocationFactory)


class ActivityFactory(DjangoModelFactory):
    class Meta:
        model = models.Activity

    name = fuzzy.FuzzyText(length=20)
    start_date = fuzzy.FuzzyDateTime(start_dt=timezone.now())
    finish_date = fuzzy.FuzzyDateTime(start_dt=timezone.now())

    event = SubFactory(EventFactory)
    place = SubFactory(PlaceFactory, location=SelfAttribute('..event.location'))
