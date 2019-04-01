from rest_framework import serializers

from .models import Event, Activity, ActivityType


class EnumField(serializers.ChoiceField):
    def to_representation(self, obj):
        return self.choices[obj].name


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'start_date', 'finish_date')


class ActivitySerializer(serializers.ModelSerializer):
    type = EnumField(choices=ActivityType.choices())
    place = serializers.CharField(source='place.name')

    class Meta:
        model = Activity
        fields = ('name', 'place', 'type', 'start_date', 'finish_date')
