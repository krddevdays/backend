import datetime

from django.apps import apps
from django.test import TestCase
from rest_framework.reverse import reverse

from events.apps import EventsConfig
from events.factories import EventFactory, VenueFactory, ZoneFactory, ActivityFactory
from events.interfaces import ActivityType, WelcomeActivity


class EventsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        date = datetime.datetime(2019, 1, 1, tzinfo=datetime.timezone.utc)
        venue = VenueFactory()
        ZoneFactory(order=0, venue=venue)
        ZoneFactory(order=1, venue=venue)
        cls.event = EventFactory(start_date=date, venue=venue)

    def _check_event(self, data: dict, event: EventFactory):
        for field in ('id', 'name', 'short_description', 'full_description', 'ticket_description',
                  'image', 'image_vk', 'image_facebook'):
            self.assertEqual(data[field], getattr(event, field))
        self.assertEqual(data['start_date'], event.start_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        self.assertEqual(data['finish_date'], event.finish_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

        venue = data['venue']
        self.assertEqual(venue['name'], event.venue.name)
        self.assertEqual(venue['address'], event.venue.address)
        self.assertEqual(venue['latitude'], event.venue.latitude)
        self.assertEqual(venue['longitude'], event.venue.longitude)
        zones = venue['zones']
        self.assertEqual(len(zones), 2)

    def test_apps(self):
        self.assertEqual(EventsConfig.name, 'events')
        self.assertEqual(apps.get_app_config('events').name, 'events')

    def test_events_list(self):
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self._check_event(data[0], self.event)

        EventFactory()
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)

    def test_event(self):
        response = self.client.get(reverse('event-detail', args=(self.event.id,)))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self._check_event(data, self.event)

    def test_ordering(self):
        first_event = EventFactory(start_date=datetime.datetime(2019, 2, 1, tzinfo=datetime.timezone.utc))
        second_event = EventFactory(start_date=datetime.datetime(2019, 3, 1, tzinfo=datetime.timezone.utc))
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 3)
        ids = [event['id'] for event in data]
        self.assertEqual(ids, [second_event.id, first_event.id, self.event.id])

    def test_search(self):
        response = self.client.get(reverse('event-list'), data={'search': self.event.name[:4]})
        data = response.json()
        self.assertEqual(len(data), 1)

        response = self.client.get(reverse('event-list'), data={'search': 'some_unique_string'})
        data = response.json()
        self.assertEqual(len(data), 0)

    def test_filter(self):
        response = self.client.get(reverse('event-list'), data={'date_from': '2019-01-01'})
        data = response.json()
        self.assertEqual(len(data), 0)

    def test_activities(self):
        activity = ActivityFactory(event=self.event, type=ActivityType.WELCOME)
        ActivityFactory(event=self.event, type=ActivityType.TALK)
        response = self.client.get(reverse('event-activities', args=(self.event.id,)))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        obj = next((item for item in data if item['type'] == 'WELCOME'))
        self.assertEqual(obj['zone'], activity.zone.name)
        self.assertEqual(obj['start_date'], activity.start_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        self.assertEqual(obj['finish_date'], activity.finish_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        self.assertEqual(obj['thing'], {'title': 'Открытие'})
        obj = next((item for item in data if item['type'] == 'TALK'))
        self.assertIsNone(obj['thing'])

    def test_tickets(self):
        pass

    def test_str(self):
        venue = VenueFactory(name='venue name', address='address')
        self.assertEqual(str(venue), 'venue name, address')
        zone = ZoneFactory(name='zone name', venue=venue)
        self.assertEqual(str(zone), 'zone name (venue name)')
        event = EventFactory(name='event name', start_date=datetime.datetime(2019, 4, 20))
        self.assertEqual(str(event), 'event name, 20.04.2019')
        activity = ActivityFactory(event=event, zone=zone, start_date=datetime.datetime(2019, 4, 20, 20, 52))
        self.assertEqual(str(activity), 'event name, 20.04.2019 - zone name (venue name) - 20.04.2019-20:52')

    def test_activity_interface(self):
        welcome = WelcomeActivity()
        self.assertEqual(str(welcome), 'Открытие')
        self.assertEqual(welcome.self_link(), 'Открытие')
