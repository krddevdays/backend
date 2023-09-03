from enumfields.drf import EnumSupportSerializerMixin
from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Vacancy, Skill


class VacancySerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Vacancy
        fields = ('company', 'description', 'skills', 'placement', 'address', 'employment', 'level', 'practice',
                  'link', 'start_cost', 'finish_cost', 'user', 'contacts', 'created_at')

    def validate(self, data):
        if data['start_cost'] > data['finish_cost']:
            raise serializers.ValidationError('Неверная зарплатная вилка')
        return data


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
