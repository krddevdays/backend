from rest_framework import serializers

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
        fields = ('event_id', 'title', 'description', 'speaker', 'video', 'presentation_offline')


class DiscussionSerializer(serializers.ModelSerializer):
    votes_count = serializers.SerializerMethodField()
    speaker = UserSerializer(read_only=True)

    class Meta:
        model = Discussion
        fields = ('event_id', 'title', 'description', 'speaker', 'votes_count')

    def get_votes_count(self, obj: Discussion) -> int:
        return obj.votes.count()
