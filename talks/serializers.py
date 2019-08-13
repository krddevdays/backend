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
    is_author = serializers.SerializerMethodField()
    my_vote = serializers.SerializerMethodField()

    class Meta:
        model = Discussion
        fields = ('id', 'event_id', 'title', 'description', 'votes_count', 'is_author', 'my_vote')

    def get_votes_count(self, obj: Discussion) -> int:
        return obj.votes.count()

    def get_is_author(self, obj: Discussion) -> bool:
        return obj.author.id == self.context['request'].user.id

    def get_my_vote(self, obj: Discussion) -> bool:
        return self.context['request'].user in obj.votes.all()
