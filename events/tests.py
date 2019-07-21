import copy
import datetime
from unittest.mock import patch

from django.apps import apps
from django.test import TestCase
from django.utils.crypto import get_random_string
from rest_framework.reverse import reverse

from .apps import EventsConfig
from .exceptions import QErr
from .factories import EventFactory, VenueFactory, ZoneFactory, ActivityFactory
from .interfaces import ActivityType, WelcomeActivity
from .qtickets import QTicketsInfo

events_response = {'id': '120', 'is_active': '1', 'name': 'Krasnodar Dev Conf 2019', 'scheme_id': '259',
                   'currency_id': 'RUB',
                   'place_name': 'Four Points Sheraton Краснодар', 'place_address': 'ул. Конгрессная, 4',
                   'place_description': '', 'city_id': '5', 'description': '', 'site_url': '', 'external_id': None,
                   'ticket_id': '19', 'mail_template_id': '32', 'shows':
                       [{'id': '149', 'is_active': '1', 'sale_start_date': None,
                         'sale_finish_date': '2019-08-16T00:00:00+03:00',
                         'open_date': '2019-08-24T10:00:00+03:00', 'start_date': '2019-08-24T11:00:00+03:00',
                         'finish_date': '2019-08-25T20:00:00+03:00', 'scheme_properties': {'admin': {
                               'zones': {'pervyj-den': {'opened': '1'}, 'vtoroj-den': {'opened': '1'},
                                         'dva-dnya': {'opened': '0'}}},
                               'zones': {'pervyj-den': {'disabled': '0',
                                                        'price_id': '534',
                                                        'rows': ['']},
                                         'vtoroj-den': {'disabled': '0',
                                                        'price_id': '533',
                                                        'rows': ['']},
                                         'dva-dnya': {'disabled': '1',
                                                      'price_id': '',
                                                      'rows': ['']}},
                               'seats': {'pervyj-den-1;1': {
                                   'max_quantity': '350'},
                                   'vtoroj-den-1;1': {
                                       'max_quantity': '350'},
                                   'dva-dnya-1;1': {
                                       'max_quantity': ''}}},
                         'prices': [{'id': 533, 'default_price': 2000, 'color_theme': '1', 'modifiers': [
                             {'type': 'sales_count', 'value': '2500', 'active_from': '', 'active_to': '',
                              'sales_count_value': '50'},
                             {'type': 'date', 'value': '2500', 'active_from': '2019-06-01T00:00:00+03:00',
                              'active_to': '2019-07-01T00:00:00+03:00', 'sales_count_value': ''},
                             {'type': 'date', 'value': '3000', 'active_from': '2019-07-01T00:00:00+03:00',
                              'active_to': '2019-08-01T00:00:00+03:00', 'sales_count_value': ''},
                             {'type': 'date', 'value': '3500', 'active_from': '2019-08-01T00:00:00+03:00',
                              'active_to': '2019-08-16T00:00:00+03:00', 'sales_count_value': ''}]},
                                    {'id': 534, 'default_price': 2000, 'color_theme': '2', 'modifiers': [
                                        {'type': 'sales_count', 'value': '2500', 'active_from': '', 'active_to': '',
                                         'sales_count_value': '50'},
                                        {'type': 'date', 'value': '2500', 'active_from': '2019-06-01T00:00:00+03:00',
                                         'active_to': '2019-07-01T00:00:00+03:00', 'sales_count_value': ''},
                                        {'type': 'date', 'value': '3000', 'active_from': '2019-07-01T00:00:00+03:00',
                                         'active_to': '2019-08-01T00:00:00+03:00', 'sales_count_value': ''},
                                        {'type': 'date', 'value': '3500', 'active_from': '2019-08-01T00:00:00+03:00',
                                         'active_to': '2019-08-16T00:00:00+03:00', 'sales_count_value': ''}]}],
                         'min_price': {'id': 534, 'default_price': 2000, 'color_theme': '2', 'modifiers': [
                             {'type': 'sales_count', 'value': '2500', 'active_from': '', 'active_to': '',
                              'sales_count_value': '50'},
                             {'type': 'date', 'value': '2500', 'active_from': '2019-06-01T00:00:00+03:00',
                              'active_to': '2019-07-01T00:00:00+03:00', 'sales_count_value': ''},
                             {'type': 'date', 'value': '3000', 'active_from': '2019-07-01T00:00:00+03:00',
                              'active_to': '2019-08-01T00:00:00+03:00', 'sales_count_value': ''},
                             {'type': 'date', 'value': '3500', 'active_from': '2019-08-01T00:00:00+03:00',
                              'active_to': '2019-08-16T00:00:00+03:00', 'sales_count_value': ''}]},
                         'max_price': {'id': 533, 'default_price': 2000, 'color_theme': '1', 'modifiers': [
                             {'type': 'sales_count', 'value': '2500', 'active_from': '', 'active_to': '',
                              'sales_count_value': '50'},
                             {'type': 'date', 'value': '2500', 'active_from': '2019-06-01T00:00:00+03:00',
                              'active_to': '2019-07-01T00:00:00+03:00', 'sales_count_value': ''},
                             {'type': 'date', 'value': '3000', 'active_from': '2019-07-01T00:00:00+03:00',
                              'active_to': '2019-08-01T00:00:00+03:00', 'sales_count_value': ''},
                             {'type': 'date', 'value': '3500', 'active_from': '2019-08-01T00:00:00+03:00',
                              'active_to': '2019-08-16T00:00:00+03:00', 'sales_count_value': ''}]}, 'deleted_at': None}],
                   'payments': [{'id': '77', 'is_active': True, 'name': 'Оплата по счету', 'handler': 'invoice',
                                 'agree_url': 'https://new.qtickets.ru/legal/kdd?event=120'},
                                {'id': '79', 'is_active': True, 'name': 'Петров П.П.', 'handler': 'best2pay',
                                 'agree_url': 'https://new.qtickets.ru/legal/kdd?event=120'}],
                   'poster': {'id': '1922', 'content_type': 'image/jpeg', 'file_size': '65833'}, 'event_type_id': '7',
                   'city': {'id': '5', 'name': 'Краснодар', 'timezone': 'Europe/Moscow'},
                   'ticket': {'id': '19', 'is_active': '1', 'name': 'Системный шаблон'},
                   'mail_template': {'id': '32', 'is_active': '1', 'name': 'Системный шаблон'},
                   'slug': 'krasnodar-dev-conf-2019', 'place_coordinates': [45.104652, 38.971342],
                   'created_at': '2019-04-24T17:11:37+03:00', 'updated_at': '2019-05-02T18:39:34+03:00',
                   'deleted_at': None}

seats_response = {
    'pervyj-den-1;1': {'seat_id': 'pervyj-den-1;1', 'admission': True, 'free_quantity': 348, 'disabled': False},
    'vtoroj-den-1;1': {'seat_id': 'vtoroj-den-1;1', 'admission': True, 'free_quantity': 350, 'disabled': False},
    'dva-dnya-1;1': {'seat_id': 'dva-dnya-1;1', 'admission': True, 'free_quantity': 0, 'disabled': True}}

correct_response = {
    "id": "10623",
    "payment_url": "https://new.qtickets.ru/pay/C6u9U7rhRJ",
    "cancel_url": "https://new.qtickets.ru/cancel-order/C6u9U7rhRJ/ce853b2f315ce49c3f3eebece00ab0d2",
    "reserved_to": "2019-07-05T13:50:49+03:00",
    "price": "1000",
    "currency_id": "RUB"
}


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

    @patch.object(QTicketsInfo, 'get_event_data', return_value=events_response)
    @patch.object(QTicketsInfo, 'get_seats_data', return_value=seats_response)
    @patch.object(QTicketsInfo, 'get_order_tickets_url', return_value=correct_response)
    def test_order(self, *args, **kwargs):
        def err_code_check(q_err_code, request_data=None, error_field='non_field_errors'):
            request = self.client.post(url, data=request_data or good_request_basic, content_type='application/json')
            self.assertEqual(request.status_code, 400)
            body = request.json()
            self.assertIn(error_field, body)
            self.assertEqual(body[error_field], [q_err_code])

        url = reverse('event-order', args=(self.event.id,))
        required_fields = ('cancel_url', 'payment_url', 'price', 'currency_id', 'reserved_to', 'id')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.event.external_id = 120
        self.event.save()
        good_request_basic = {
            "first_name": "Alex", "last_name": "Johns", "email": "a@a.ru", "phone": "+78612522262", "payment_id": "79",
            "tickets": [
                {"first_name": "Ser", "last_name": "Ber", "email": "morzh@morhzhoviy.com", "type_id": "pervyj-den-1;1"}
            ]
        }

        good_request_inn = good_request_basic.copy()
        good_request_inn.update({'inn': '7810671063', 'legal_name': 'Рога и Копыта'})
        bad_phone_request = good_request_basic.copy()

        bad_phone_request.update({'phone': '+7944123123'})
        request = self.client.post(url, data=bad_phone_request)
        self.assertEqual(request.status_code, 400)
        self.assertIn('phone', request.json())
        del bad_phone_request

        request = self.client.post(url, data=good_request_basic, content_type='application/json')
        self.assertEqual(request.status_code, 200)
        content = request.json()
        for field in required_fields:
            self.assertIn(field, content)

        events_response['is_active'] = '0'
        err_code_check(QErr.NOT_ACTIVE)
        events_response['is_active'] = '1'

        events_response['shows'][0]['is_active'] = '0'
        err_code_check(QErr.NOT_ACTIVE)
        events_response['shows'][0]['is_active'] = '1'

        events_response['shows'][0]['sale_start_date'] = '2119-05-02T18:39:34+03:00'
        err_code_check(QErr.SALE_NOT_STARTED)
        events_response['shows'][0]['sale_start_date'] = '2019-05-02T18:39:34+03:00'

        bad_payment_id_request = good_request_basic.copy()
        bad_payment_id_request['payment_id'] = '123456'
        err_code_check(QErr.P_ID_NOT_FOUND, bad_payment_id_request, 'payment_id')
        del bad_payment_id_request

        request = self.client.post(url, data=good_request_inn, content_type='application/json')
        self.assertEqual(request.status_code, 200)
        for field in required_fields:
            self.assertIn(field, content)

        bad_request_inn = good_request_inn.copy()
        bad_request_inn['payment_id'] = '77'
        del bad_request_inn['inn']
        err_code_check(QErr.LEGAL, bad_request_inn, 'payment_id')
        del bad_request_inn

        bad_request_legal = good_request_inn.copy()
        bad_request_legal['payment_id'] = '77'
        del bad_request_legal['legal_name']
        err_code_check(QErr.LEGAL, bad_request_legal, 'payment_id')
        del bad_request_legal

        doubled_email_request = copy.deepcopy(good_request_basic)
        doubled_email_request['tickets'].append(doubled_email_request['tickets'][0])
        err_code_check(QErr.TICKETS_EMAIL_NON_UNIQ, doubled_email_request)
        del doubled_email_request

        bad_request_ticket_type_id = copy.deepcopy(good_request_basic)
        bad_request_ticket_type_id['tickets'][0]['type_id'] = get_random_string()
        err_code_check(QErr.TICKETS_TYPE_ID_NONEXISTS.format(type_id=bad_request_ticket_type_id['tickets'][0]['type_id']),
                       bad_request_ticket_type_id)
        del bad_request_ticket_type_id

        seats_response[good_request_basic['tickets'][0]['type_id']]['disabled'] = True
        err_code_check(QErr.TICKETS_TYPE_ID_DISABLED)
        seats_response[good_request_basic['tickets'][0]['type_id']]['disabled'] = False

        seats_response[good_request_basic['tickets'][0]['type_id']]['free_quantity'] = 1
        no_more_seets_request = copy.deepcopy(good_request_basic)
        no_more_seets_request['tickets'].append(
            {"first_name": "Random", "last_name": "Randomich", "email": "random@randomich.me", "type_id": "pervyj-den-1;1"}
        )
        err_code_check(QErr.MEST_NEMA.format(
            type_id=no_more_seets_request['tickets'][0]['type_id']),
            no_more_seets_request
        )
        del no_more_seets_request

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
