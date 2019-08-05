from rest_framework import serializers

from talks.models import Talk, Speaker


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = '__all__'


class TalkSerializer(serializers.ModelSerializer):
    speaker = SpeakerSerializer()

    class Meta:
        model = Talk
        fields = ('event_id', 'title', 'description', 'poster_image', 'speaker', 'video', 'presentation_offline')
