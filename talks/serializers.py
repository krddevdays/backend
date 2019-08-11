from rest_framework import serializers

from events.models import Event
from talks.models import Talk, Speaker, Discussion
from users.serializers import UserSerializer


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = '__all__'


class TalkSerializer(serializers.ModelSerializer):
    speaker = SpeakerSerializer()

    class Meta:
        model = Talk
        fields = ('event_id', 'title', 'description', 'poster_image', 'speaker', 'video', 'presentation_offline')


class DiscussionSerializer(serializers.ModelSerializer):
    event_id = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), source='event')
    votes_count = serializers.SerializerMethodField()

    class Meta:
        model = Discussion
        fields = ('event_id', 'title', 'description', 'votes_count')

    def get_votes_count(self, obj: Discussion) -> int:
        return obj.votes.count()
