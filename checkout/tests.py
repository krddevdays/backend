from django.apps import apps
from django.conf import settings
from django.test import TestCase
from django.utils.crypto import get_random_string
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

    def test_link(self):
        data = {'id': self.ticket.qticket_id, 'email': self.ticket.email}
        response = self.client.post(reverse('link_user_qtickets'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 403)

        user = UserFactory()
        self.client.force_login(user, settings.AUTHENTICATION_BACKENDS[0])

        data = {'id': self.ticket.qticket_id, 'email': get_random_string()}
        response = self.client.post(reverse('link_user_qtickets'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)

        data = {'id': self.ticket.qticket_id, 'email': self.ticket.email}
        response = self.client.post(reverse('link_user_qtickets'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.user_id, user.id)
