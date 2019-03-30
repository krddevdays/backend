import string

from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

User = get_user_model()


class UserFactory(DjangoModelFactory):
    email = FuzzyText(suffix='@email.org', chars=string.ascii_lowercase)

    class Meta:
        model = 'users.User'
