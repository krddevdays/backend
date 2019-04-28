from django.apps import apps
from django.conf import settings
from django.test import TestCase
from rest_framework.reverse import reverse

from checkout.apps import CheckoutConfig
from checkout.factories import OrderFactory, TicketFactory
from events.factories import EventFactory
from users.factories import UserFactory


class CheckoutTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.event = EventFactory()
        cls.order = OrderFactory()
        cls.ticket = TicketFactory()

    def test_apps(self):
        self.assertEqual(CheckoutConfig.name, 'checkout')
        self.assertEqual(apps.get_app_config('checkout').name, 'checkout')

    def test_my_orders(self):
        user = UserFactory()
        self.client.force_login(user, settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        user = UserFactory(email=self.order.email)
        self.client.force_login(user, settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_my_tickets(self):
        user = UserFactory()
        self.client.force_login(user, settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(reverse('ticket-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        user = UserFactory(email=self.ticket.email)
        self.client.force_login(user, settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(reverse('ticket-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_create_order(self):
        def append_base_info(data, klass):
            for field in ('email', 'first_name', 'last_name'):
                data[field] = getattr(klass, field).fuzz()

        payload = {'event': self.event.id, 'tickets': [{}]}
        response = self.client.post(reverse('order-list'), data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = response.json()
        for field in ('email', 'first_name', 'last_name', 'tickets'):
            self.assertIn(field, data)

        append_base_info(payload, OrderFactory)
        append_base_info(payload['tickets'][0], TicketFactory)
        response = self.client.post(reverse('order-list'), data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['event'], payload['event'])
        self.assertEqual(data['email'], payload['email'])
        self.assertEqual(data['first_name'], payload['first_name'])
        self.assertEqual(data['last_name'], payload['last_name'])
        tickets = data['tickets']
        self.assertEqual(len(tickets), 1)
        self.assertEqual(data['tickets'][0]['email'], tickets[0]['email'])
        self.assertEqual(data['tickets'][0]['first_name'], tickets[0]['first_name'])
        self.assertEqual(data['tickets'][0]['last_name'], tickets[0]['last_name'])

        duplicate = {}
        append_base_info(duplicate, TicketFactory)
        duplicate['email'] = payload['tickets'][0]['email']
        payload['tickets'].append(duplicate)
        response = self.client.post(reverse('order-list'), data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('tickets', data)
