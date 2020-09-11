from rest_framework import serializers

from krddevdays.serializers import EnumField
from users.serializers import UserSerializer
from .enums import PlacementType, EmploymentType
from .models import Vacancy, Technology


class VacancySerializer(serializers.ModelSerializer):
    placement = EnumField(choices=PlacementType.choices())
    employment = EnumField(choices=EmploymentType.choices())
    user = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Vacancy
        fields = ('company', 'description', 'technologies', 'placement', 'address', 'employment',
                  'link', 'start_cost', 'finish_cost', 'user', 'created_at')

    def validate(self, data):
        if data['start_cost'] > data['finish_cost']:
            raise serializers.ValidationError('Неверная зарплатная вилка')
        return data


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = '__all__'
