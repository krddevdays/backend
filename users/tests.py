from django.core.exceptions import NON_FIELD_ERRORS
from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import get_random_string

from users.factories import UserFactory


class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def test_login(self):
        credentials = {'username': self.user.email, 'password': get_random_string()}
        response = self.client.post(reverse('login'), credentials)
        self.assertEqual(response.status_code, 400)
        self.assertIn(NON_FIELD_ERRORS, response.json())

        password = get_random_string()
        self.user.set_password(password)
        self.user.save()
        credentials = {'username': self.user.email, 'password': password}
        response = self.client.post(reverse('login'), credentials)
        self.assertEqual(response.status_code, 200)
