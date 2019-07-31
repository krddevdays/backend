import datetime

from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText, FuzzyFloat, FuzzyDateTime, FuzzyChoice

from events.interfaces import ActivityType


class VenueFactory(DjangoModelFactory):
    name = FuzzyText()
    address = FuzzyText()
    latitude = FuzzyFloat(low=-180.0, high=180.0)
    longitude = FuzzyFloat(low=-180.0, high=180.0)

    class Meta:
        model = 'events.Venue'


class ZoneFactory(DjangoModelFactory):
    name = FuzzyText()
    venue = SubFactory(VenueFactory)

    class Meta:
        model = 'events.Zone'


class EventFactory(DjangoModelFactory):
    name = FuzzyText()
    start_date = FuzzyDateTime(start_dt=datetime.datetime(2019, 1, 1, tzinfo=datetime.timezone.utc),
                               end_dt=datetime.datetime(2019, 12, 31, tzinfo=datetime.timezone.utc))
    finish_date = FuzzyDateTime(start_dt=datetime.datetime(2019, 1, 1, tzinfo=datetime.timezone.utc),
                                end_dt=datetime.datetime(2019, 12, 31, tzinfo=datetime.timezone.utc))
    venue = SubFactory(VenueFactory)

    class Meta:
        model = 'events.Event'


class ActivityFactory(DjangoModelFactory):
    event = SubFactory(EventFactory)
    zone = SubFactory(ZoneFactory)
    type = FuzzyChoice(choices=ActivityType.values)
    start_date = FuzzyDateTime(start_dt=datetime.datetime(2019, 1, 1, tzinfo=datetime.timezone.utc),
                               end_dt=datetime.datetime(2019, 12, 31, tzinfo=datetime.timezone.utc))
    finish_date = FuzzyDateTime(start_dt=datetime.datetime(2019, 1, 1, tzinfo=datetime.timezone.utc),
                                end_dt=datetime.datetime(2019, 12, 31, tzinfo=datetime.timezone.utc))

    class Meta:
        model = 'events.Activity'


class PartnerFactory(DjangoModelFactory):
    event = SubFactory(EventFactory)
    name = FuzzyText()

    class Meta:
        model = 'events.Partner'
