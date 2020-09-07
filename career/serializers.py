from rest_framework import serializers

from krddevdays.serializers import EnumField
from users.serializers import UserSerializer
from .enums import PlacementType, EmploymentType
from .models import Vacancy


class VacancySerializer(serializers.ModelSerializer):
    placement = EnumField(choices=PlacementType.choices())
    employment = EnumField(choices=EmploymentType.choices())
    user = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Vacancy
        fields = ('company', 'description', 'technologies', 'placement', 'address', 'employment',
                  'link', 'start_cost', 'finish_cost', 'user', 'created_at')
