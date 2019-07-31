import string

from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

User = get_user_model()


class UserFactory(DjangoModelFactory):
    username = FuzzyText(chars=string.ascii_lowercase)
    first_name = FuzzyText(chars=string.ascii_lowercase)
    last_name = FuzzyText(chars=string.ascii_lowercase)
    email = FuzzyText(suffix='@email.org', chars=string.ascii_lowercase)

    class Meta:
        model = 'users.User'
