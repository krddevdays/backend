import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers


class QTickets:

    def __init__(self):
        if not (settings.QTICKETS_TOKEN or settings.QTICKETS_ENDPOINT):
            raise ImproperlyConfigured('''QTickets credentials must be
             set in environment variables''')
        self.API_endpoint = f'{settings.QTICKETS_ENDPOINT}/api/rest/v1/'
        self.session = requests.Session()
        self.session.headers = {'Authorization': f'Bearer {settings.QTICKETS_TOKEN}'}

    def get_event_url(self, event_id: int) -> str:
        return f'{self.API_endpoint}events/{event_id}'

    def check_event_exist(self, external_id: int):
        """ Check qtickets.com system for this event id by calling their API """

        self.session.head(url=self.get_event_url(external_id)).raise_for_status()

    def _make_request(self, method: str, url: str, **kwargs):
        return self.session.request(method=method, url=url, **kwargs).json()

    def get_event_data(self, external_id: int):
        return self._make_request(
            method='GET',
            url=self.get_event_url(external_id)
        )['data']

    def get_seats_data(self, show_id: str):
        return self._make_request('GET', self.get_seats_url(show_id), json={
            "select": [
                "name",
                "free_quantity",
                "price",
                "disabled"
            ]
        })['data']

    def get_seats_url(self, show_id) -> str:
        return f'{self.API_endpoint}shows/{show_id}/seats'


QTicketsInfo = QTickets()


class ModifiersSerializer(serializers.Serializer):
    type = serializers.CharField()
    value = serializers.DecimalField(max_digits=10, decimal_places=2)
    sales_count_value = serializers.IntegerField(required=False)
    frm = serializers.DateTimeField(required=False)
    to = serializers.DateTimeField(required=False)


ModifiersSerializer._declared_fields['from'] = ModifiersSerializer._declared_fields['frm']
del ModifiersSerializer._declared_fields['frm']


class PriceSerializer(serializers.Serializer):
    current_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    default_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    modifiers = ModifiersSerializer(many=True)


class SeatsTypesSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    disabled = serializers.BooleanField()
    price = PriceSerializer(many=False)


class PaymentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.CharField()


class TicketsSerializer(serializers.Serializer):
    def __init__(self, **kwargs):
        show_data = kwargs['data'].get('event_data')
        seats_data = kwargs['data'].get('seats_data')
        show = show_data['shows'][0]

        prices_dict = dict()
        for zone in show['scheme_properties']['zones']:
            for p in show['prices']:
                if str(p['id']) == show['scheme_properties']['zones'][zone]['price_id']:
                    prices_dict[zone] = p
                    continue

        prepared_data = dict(
            is_active=show_data['is_active'] and show['is_active'],
            sale_start_date=show['sale_start_date'],
            sale_finish_date=show['sale_finish_date'],
            payments=[
                {
                    'id': payment['id'],
                    'type': 'invoice' if payment['handler'] == 'invoice' else 'card'
                }
                for payment in show_data['payments']
                if payment['is_active']
            ],
            types=[
                {
                    'id': seats['seat_id'],
                    'name': seats['name'],
                    'disabled': seats['free_quantity'] == 0,
                    'price': {
                        'current_value': seats['price'],
                        'default_value': prices_dict[zone['zone_id']]['default_price'],
                        'modifiers': [
                            {
                                'type': modifier['type'],
                                'sales_count_value': int(modifier['sales_count_value']),
                                'value': modifier['value']  # Decimal
                            } if modifier['type'] == 'sales_count'
                            else {
                                'type': modifier['type'],
                                'from': modifier.get('active_from'),
                                'to': modifier.get('active_to'),
                                'value': modifier['value']
                            }  # if modifier['type'] == 'date'
                            for modifier in
                            prices_dict[zone['zone_id']]['modifiers']
                        ]
                    }
                }
                for zone in seats_data.values()
                for seats in zone['seats'].values()
                if not seats['disabled']
            ]
        )
        super().__init__(data=prepared_data)

    is_active = serializers.BooleanField()
    sale_start_date = serializers.DateTimeField(allow_null=True)
    sale_finish_date = serializers.DateTimeField(allow_null=True)
    payments = PaymentSerializer(many=True)
    types = SeatsTypesSerializer(many=True)
