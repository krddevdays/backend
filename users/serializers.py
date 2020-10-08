from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, Company


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'work', 'position')
        read_only_fields = ('username', 'email')


class CompanySerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(required=False)

    class Meta:
        model = Company
        fields = ('id', 'title', 'description', 'address', 'coordinates', 'site', 'phone', 'email')

    def validate(self, attrs):
        address = bool(attrs.get('address'))
        coordinates = bool(attrs.get('coordinates'))
        if address != coordinates:
            raise ValidationError('Координаты обязательны при указании адреса.')
        return attrs
