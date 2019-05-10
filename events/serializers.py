import dateutil
from django.db import models
from django.utils import timezone
from django.utils.module_loading import import_string
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty

from events.qtickets import QTicketsInfo
from .models import Event, Activity, ActivityType, Venue


class EnumField(serializers.ChoiceField):
    def to_representation(self, obj):
        return self.choices[obj].name


class BaseActivitySerializer(serializers.Serializer):
    title = serializers.CharField()


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ('name', 'address', 'latitude', 'longitude')


class EventSerializer(serializers.ModelSerializer):
    venue = VenueSerializer()

    class Meta:
        model = Event
        fields = ('id', 'name', 'start_date', 'finish_date', 'venue')


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
        super().__init__(instance, data, **kwargs)

    def validate(self, attrs):
        current_show = self.event_info['shows'][0]

        # Шоу и ивент должны быть активны
        if (
                not int(self.event_info['is_active'])
                or not int(current_show['is_active'])
        ):
            raise ValidationError(QErr.NOT_ACTIVE)
        # Дата старта продаж должна быть больше текущей
        elif (
                current_show['sale_start_date'] is not None
                and dateutil.parser.parse(current_show['sale_start_date']) > timezone.now()
        ):
            raise ValidationError(QErr.SALE_NOT_STARTED)
        return attrs

    def validate_payment_id(self, payment_id):
        if payment_id not in [p['id'] for p in self.event_info['payments']]:
            raise ValidationError(QErr.P_ID_NOT_FOUND)
        return payment_id
