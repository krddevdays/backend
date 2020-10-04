from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from .models import User, Company


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'work', 'position')
        read_only_fields = ('username', 'email')


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'work', 'position')


class CompanySerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(required=False)
    owner = OwnerSerializer(required=False)

    class Meta:
        model = Company
        fields = ('title', 'description', 'address', 'coordinates', 'site', 'phone', 'email', 'owner')
        read_only_fields = ('owner',)
