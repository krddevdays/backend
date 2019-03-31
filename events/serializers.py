from rest_framework import serializers

from events.models import Event, Activity, ActivityType


class EnumField(serializers.ChoiceField):
    def to_representation(self, obj):
        return self.choices[obj].name


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'start_date', 'finish_date')


class ActivitySerializer(serializers.ModelSerializer):
    type = EnumField(choices=ActivityType.choices())
    area = serializers.CharField(source='area.name')

    class Meta:
        model = Activity
        fields = ('name', 'area', 'type', 'start_date', 'finish_date')
