from django.db import models
from django.utils.module_loading import import_string
from rest_framework import serializers

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
        fields = ('id', 'name', 'short_description', 'full_description', 'ticket_description',
                  'image', 'image_vk', 'image_facebook', 'start_date', 'finish_date', 'venue')


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
