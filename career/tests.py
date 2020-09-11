from django.apps import apps
from django.test import TestCase
from django.utils.crypto import get_random_string
from rest_framework.reverse import reverse

from .apps import CareerConfig
from users.factories import UserFactory
from users.models import User


class CareerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user: User = UserFactory()

    def test_apps(self):
        self.assertEqual(CareerConfig.name, 'career')
        self.assertEqual(apps.get_app_config('career').name, 'career')

    def test_create_vacancy(self):
        data = {
            'company': get_random_string(),
            'description': get_random_string(),
            'technologies': [get_random_string(10) for _ in range(3)],
            'placement': 0,
            'address': get_random_string(),
            'employment': 0,
            'start_cost': 90_000,
            'finish_cost': 120_000
        }
        response = self.client.post(reverse('vacancy-list'), data=data)
        self.assertEqual(response.status_code, 403)  # https://github.com/encode/django-rest-framework/issues/5968

        credentials = {'username': self.user.username, 'password': self.user.original_password}
        response = self.client.post(reverse('login'), credentials)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('vacancy-list'), data=data)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['user']['username'], self.user.username)

    def test_create_vacancy(self):
        data = {
            'company': get_random_string(),
            'description': get_random_string(),
            'technologies': [get_random_string(10) for _ in range(3)],
            'placement': 0,
            'address': get_random_string(),
            'employment': 0,
            'start_cost': 120_000,
            'finish_cost': 90_000
        }
        credentials = {'username': self.user.username, 'password': self.user.original_password}
        response = self.client.post(reverse('login'), credentials)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('vacancy-list'), data=data)
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('non_field_errors', data)
