from rest_framework import serializers

from .models import Event, Activity, ActivityType, Venue


class EnumField(serializers.ChoiceField):
    def to_representation(self, obj):
        return self.choices[obj].name


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

    class Meta:
        model = Activity
        fields = ('name', 'zone', 'type', 'start_date', 'finish_date')
