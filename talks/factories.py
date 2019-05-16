import string

from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

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
    speaker = SubFactory(SpeakerFactory)

    class Meta:
        model = 'talks.Talk'


class DiscussionFactory(DjangoModelFactory):
    title = FuzzyText()
    description = FuzzyText()
    speaker = SubFactory(UserFactory)

    class Meta:
        model = 'talks.Discussion'
