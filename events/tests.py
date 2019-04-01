from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import EventFactory, ActivityFactory
from .models import Event


class EventsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.event1, cls.event2 = EventFactory(), EventFactory()
        cls.activity1 = ActivityFactory(event=cls.event1)
        cls.activity2 = ActivityFactory(event=cls.event1)
        cls.activity3 = ActivityFactory(event=cls.event2)
        cls.activity4 = ActivityFactory(event=cls.event2)

    def test_events_list(self):
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Event.objects.count())

    def test_events_retrieve(self):
        url = reverse('event-detail', kwargs={'pk': self.event1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertTrue(response.data)

    def test_event_details(self):
        url = reverse('event-activities', kwargs={'pk': self.event1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
