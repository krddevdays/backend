from django.apps import apps
from django.contrib.auth import get_user
from django.core.exceptions import NON_FIELD_ERRORS
from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import get_random_string

from users.apps import UsersConfig
from users.factories import UserFactory


class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = get_random_string()
        cls.user = UserFactory()
        cls.user.set_password(cls.password)
        cls.user.save()

    def _is_authenticated(self):
        user = get_user(self.client)
        return user.is_authenticated

    def test_apps(self):
        self.assertEqual(UsersConfig.name, 'users')
        self.assertEqual(apps.get_app_config('users').name, 'users')

    def test_registration(self):
        credentials = {
            'username': 'random@random.com',
            'password1': self.password,
            'password2': self.password
        }
        response = self.client.post(reverse('registration'), credentials)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self._is_authenticated())

        credentials['password2'] = 'bad password'
        response = self.client.post(reverse('registration'), credentials)
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        credentials = {'username': self.user.email, 'password': get_random_string()}
        response = self.client.post(reverse('login'), credentials)
        self.assertEqual(response.status_code, 400)
        self.assertIn(NON_FIELD_ERRORS, response.json())

        credentials = {'username': self.user.email, 'password': self.password}
        response = self.client.post(reverse('login'), credentials)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self._is_authenticated())

    def test_logout(self):
        credentials = {'username': self.user.email, 'password': self.password}
        self.client.post(reverse('login'), credentials)
        self.assertTrue(self._is_authenticated())

        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self._is_authenticated())
