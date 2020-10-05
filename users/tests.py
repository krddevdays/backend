import string
from decimal import Decimal

from django.apps import apps
from django.contrib.auth import get_user
from django.core.exceptions import NON_FIELD_ERRORS
from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import get_random_string

from .apps import UsersConfig
from .factories import UserFactory, CompanyFactory
from .models import CompanyStatus, Company


class CompanyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def test_create(self):
        data = {
            'title': get_random_string(),
            'coordinates': [45.34, 34.45]
        }
        response = self.client.post(reverse('company-list'), data=data)
        self.assertEqual(response.status_code, 403)  # https://github.com/encode/django-rest-framework/issues/5968

        credentials = {'username': self.user.username, 'password': self.user.original_password}
        response = self.client.post(reverse('login'), credentials)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('company-list'), data=data)
        result = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', result)

        data['address'] = get_random_string()
        response = self.client.post(reverse('company-list'), data=data)
        self.assertEqual(response.status_code, 201)
        result = response.json()
        self.assertEqual(result['title'], data['title'])
        self.assertEqual(result['coordinates'], ['45.340000', '34.450000'])
        new = Company.objects.get(pk=result['id'])
        self.assertEqual(new.title, data['title'])
        self.assertEqual(new.owner_id, self.user.id)

    def test_pagination(self):
        [CompanyFactory() for _ in range(12)]
        response = self.client.get(reverse('company-list'))
        result = response.json()['results']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 10)

        response = self.client.get(reverse('company-list'), data={'page': 2})
        result = response.json()['results']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 2)

    def test_list(self):
        company = CompanyFactory(
            description=get_random_string(),
            address=get_random_string(),
            coordinates=(Decimal(45.34), Decimal(34.45)),
            site=f'https://{get_random_string()}.com/',
            phone=f'+79{get_random_string(length=9, allowed_chars=string.digits)}',
            owner=self.user)
        response = self.client.get(reverse('company-list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()['results']
        self.assertEqual(len(data), 1)
        obj = data[0]
        self.assertEqual(obj['title'], company.title)
        self.assertEqual(obj['description'], company.description)
        self.assertEqual(obj['address'], company.address)
        self.assertEqual(obj['coordinates'], ['45.340000', '34.450000'])
        self.assertEqual(obj['site'], company.site)
        self.assertEqual(obj['phone'], company.phone)
        self.assertEqual(obj['email'], company.email)

        company.status = CompanyStatus.HIDDEN
        company.save()
        response = self.client.get(reverse('company-list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()['results']
        self.assertEqual(len(data), 0)


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
            'username': 'Random',
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
        self.assertEqual(user.username, credentials['username'].lower())
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

        credentials = {'username': self.user.username.capitalize(), 'password': self.user.original_password}
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

        credentials = {'username': self.user.username, 'password': self.user.original_password}
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
