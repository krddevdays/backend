import string

import factory
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
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

    def __init__(self):
        super(UserFactory, self).__init__()
        self.original_password = None

    @factory.post_generation
    def set_password(self, create, extracted, **kwargs):
        self.original_password = get_random_string(allowed_chars=string.ascii_lowercase)
        self.set_password(self.original_password)
