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
        cls.user = UserFactory()

    def _is_authenticated(self):
        user = get_user(self.client)
        return user.is_authenticated

    def test_apps(self):
        self.assertEqual(UsersConfig.name, 'users')
        self.assertEqual(apps.get_app_config('users').name, 'users')

    def test_registration(self):
        credentials = {
            'username': 'random',
            'email': 'random@random.com',
            'first_name': get_random_string(),
            'last_name': get_random_string(),
            'password1': self.user.original_password,
            'password2': self.user.original_password
        }
        response = self.client.post(reverse('registration'), credentials, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self._is_authenticated())
        user = get_user(self.client)
        self.assertEqual(user.email, credentials['email'])
        self.assertEqual(user.username, credentials['username'])
        self.assertEqual(user.first_name, credentials['first_name'])
        self.assertEqual(user.last_name, credentials['last_name'])

        credentials['password2'] = 'bad password'
        response = self.client.post(reverse('registration'), credentials, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        credentials = {'username': self.user.username, 'password': get_random_string()}
        response = self.client.post(reverse('login'), credentials, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(NON_FIELD_ERRORS, response.json())

        credentials = {'username': self.user.username, 'password': self.user.original_password}
        response = self.client.post(reverse('login'), credentials, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self._is_authenticated())

    def test_logout(self):
        credentials = {'username': self.user.username, 'password': self.user.original_password}
        self.client.post(reverse('login'), credentials, content_type='application/json')
        self.assertTrue(self._is_authenticated())

        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self._is_authenticated())

    def test_me(self):
        url = reverse('me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        credentials = {'username': self.user.username, 'password': self.password}
        self.client.post(reverse('login'), credentials, content_type='application/json')
        self.assertTrue(self._is_authenticated())

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        for key in ('first_name', 'last_name', 'email', 'work', 'position'):
            self.assertIn(key, data)

        values = {
            'first_name': get_random_string(),
            'last_name': get_random_string(),
            'work': get_random_string(),
            'position': get_random_string(),
        }
        response = self.client.patch(url, values, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        for key in ('first_name', 'last_name', 'work', 'position'):
            self.assertEqual(data[key], values[key])

        values = {
            'email': 'email@mail.ru',
        }
        response = self.client.patch(url, values, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertNotEqual(data['email'], values['email'])
