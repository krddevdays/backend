import string

import factory
from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from events.factories import EventFactory
from users.factories import UserFactory


class SpeakerFactory(DjangoModelFactory):
    first_name = FuzzyText()
    last_name = FuzzyText()
    avatar = FuzzyText(prefix='https://', suffix='.ru', chars=string.ascii_lowercase)

    class Meta:
        model = 'talks.Speaker'


class TalkFactory(DjangoModelFactory):
    title = FuzzyText()
    description = FuzzyText()
    # speakers = SubFactory(SpeakerFactory)

    class Meta:
        model = 'talks.Talk'

    @factory.post_generation
    def speakers(self, create, extracted, **kwargs):
        self.speakers.add(SpeakerFactory())


class DiscussionFactory(DjangoModelFactory):
    event = SubFactory(EventFactory)
    title = FuzzyText()
    description = FuzzyText()
    author = SubFactory(UserFactory)

    class Meta:
        model = 'talks.Discussion'
