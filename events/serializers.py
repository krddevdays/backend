from collections import Counter

import dateutil.parser
from django.db import models
from django.utils import timezone
from django.utils.module_loading import import_string
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty

from events.qtickets import QTicketsInfo
from .models import Event, Activity, ActivityType, Venue, Zone


class EnumField(serializers.ChoiceField):
    def to_representation(self, obj):
        return self.choices[obj].name


class BaseActivitySerializer(serializers.Serializer):
    title = serializers.CharField()


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ('name', 'order')


class VenueSerializer(serializers.ModelSerializer):
    zones = ZoneSerializer(many=True)

    class Meta:
        model = Venue
        fields = ('name', 'address', 'latitude', 'longitude', 'zones')


class EventSerializer(serializers.ModelSerializer):
    venue = VenueSerializer()

    class Meta:
        model = Event
        fields = ('id', 'name', 'short_description', 'full_description', 'ticket_description',
                  'image', 'image_vk', 'image_facebook', 'start_date', 'finish_date', 'venue',
                  'cfp_start', 'cfp_finish', 'cfp_url')


class ActivitySerializer(serializers.ModelSerializer):
    type = EnumField(choices=ActivityType.choices())
    zone = serializers.CharField(source='zone.name')
    thing = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ('zone', 'type', 'start_date', 'finish_date', 'thing')

    def get_thing(self, obj: Activity):
        thing = obj.thing
        if thing is None:
            return None
        if isinstance(thing, models.Model):
            serializer = import_string(f'{thing._meta.app_label}.serializers.{thing._meta.object_name}Serializer')
        else:
            serializer = BaseActivitySerializer
        return serializer(thing).data


def check_inn(inn):
    """
    Проверка ИНН на валидность
    :param inn: строка с ИНН
    :raises ValidationError: в случае если ИНН неверный
    :return: возвращяет ИНН
    """

    def inn_csum(_inn):
        k = (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
        pairs = zip(k[11 - len(_inn):], [int(x) for x in _inn])
        return str(sum([k * v for k, v in pairs]) % 11 % 10)

    if len(inn) not in (10, 12):
        raise ValidationError('Неверный ИНН, длинна должна быть 10 или 12 символов', code='inn')

    if len(inn) == 10:
        integrity = inn[-1] == inn_csum(inn[:-1])
    else:
        integrity = inn[-2:] == inn_csum(inn[:-2]) + inn_csum(inn[:-1])
    if not integrity:
        raise ValidationError('Неверный ИНН, неверный код', code='inn')
    return inn


class TicketsSerializer(serializers.Serializer):
    type_id = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()


class QErr:
    NOT_ACTIVE = 'Ивент не активен в данный момент'
    SALE_NOT_STARTED = 'Продажа билетов еще не началась'
    P_ID_NOT_FOUND = 'Не найден payment_id'
    LEGAL = 'Неверные данные для зказа, ИНН и/или наименование организации не указанны'
    TICKETS_EMAIL_NON_UNIQ = 'Email в запросе на покупку билетов не уникальны'
    TICKETS_TYPE_ID_NONEXISTS = 'Неверный type_id в заказе, {type_id} не существует'
    TICKETS_TYPE_ID_DISABLED = 'Неверный type_id в заказе, {type_id} не доступны для покупки'
    MEST_NEMA = 'Для типа {type_id} недостаточно свободных мест'


class QTicketsOrderSerializer(serializers.Serializer):
    first_name = serializers.CharField(help_text='Имя')
    last_name = serializers.CharField(help_text='Фамилия')
    email = serializers.EmailField(help_text='Адрес электронной почты')
    phone = PhoneNumberField(help_text='Номер телефона', required=False)
    payment_id = serializers.CharField()
    tickets = TicketsSerializer(many=True)

    inn = serializers.CharField(validators=[check_inn, ], required=False)
    legal_name = serializers.CharField(required=False)

    def __init__(self, event_id, instance=None, data=empty, **kwargs):
        self.event_info = QTicketsInfo.get_event_data(event_id)
        self.seats_info = QTicketsInfo.get_seats_data(
            select_fields=["free_quantity", "disabled"],
            show_id=self.event_info['shows'][0]['id'],
            flat=True
        )
        self.current_show = self.event_info['shows'][0]
        super().__init__(instance, data, **kwargs)

    def validate(self, data):

        # Шоу и ивент должны быть активны
        if (
                not int(self.event_info['is_active'])
                or not int(self.current_show['is_active'])
        ):
            raise ValidationError(QErr.NOT_ACTIVE)
        # Дата старта продаж должна быть больше текущей
        elif (
                self.current_show['sale_start_date'] is not None
                and dateutil.parser.parse(self.current_show['sale_start_date']) > timezone.now()
        ):
            raise ValidationError(QErr.SALE_NOT_STARTED)

        # email должны быть уникальны в рамках tickets из данного запроса
        tickets_emails = [ticket['email'] for ticket in data['tickets']]
        if len(tickets_emails) > len(set(tickets_emails)):
            raise ValidationError({'tickets': QErr.TICKETS_EMAIL_NON_UNIQ})

        seats_by_type = Counter([el['type_id'] for el in data['tickets']])

        for ticket_request in data['tickets']:
            type_id = ticket_request['type_id']
            if type_id not in self.seats_info:
                raise ValidationError(QErr.TICKETS_TYPE_ID_NONEXISTS.format(type_id=type_id))
            elif self.seats_info[type_id]['disabled']:
                raise ValidationError(QErr.TICKETS_TYPE_ID_DISABLED.format(type_id=type_id))
            elif seats_by_type[type_id] > self.seats_info[type_id]['free_quantity']:
                raise ValidationError(QErr.MEST_NEMA.format(type_id=type_id))

        return data

    def validate_payment_id(self, payment_id):
        for payment in self.event_info['payments']:
            if payment['id'] == payment_id:
                break
        else:
            raise ValidationError(QErr.P_ID_NOT_FOUND)
        if payment['handler'] == 'invoice' and {'inn', 'legal_name'} - set(self.initial_data):
            raise ValidationError(QErr.LEGAL)
        return payment_id

    def order_tickets(self, host: str, external_id: int) -> str:
        juridicial = False
        order_body = {
            'email': self.validated_data['email'],
            'name': self.validated_data['first_name'],
            'surname': self.validated_data['last_name'],
            'phone': str(self.validated_data.get('phone', '')),
            'host': host,
            'payment_id': self.validated_data['payment_id'],
            'event_id': external_id,
            'baskets': [
                {
                    'show_id': self.current_show['id'],
                    'seat_id': basket['type_id'],
                    'client_email': basket['email'],
                    'client_name': basket['first_name'],
                    'client_surname': basket['last_name']

                }
                for basket
                in self.validated_data['tickets']
            ]
        }
        if 'inn' in self.validated_data:
            order_body.update({'legal_name': self.validated_data['legal_name'], 'inn': self.validated_data['inn']})
            juridicial = True
        return QTicketsInfo.get_order_tickets_url(
            tickets_data=order_body,
            juridicial=juridicial
        )
