import string

from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from events.factories import EventFactory


class OrderFactory(DjangoModelFactory):
    event = SubFactory(EventFactory)
    email = FuzzyText(suffix='@email.org', chars=string.ascii_lowercase)
    first_name = FuzzyText()
    last_name = FuzzyText()

    class Meta:
        model = 'checkout.Order'


class TicketFactory(DjangoModelFactory):
    order = SubFactory(OrderFactory)
    email = FuzzyText(suffix='@email.org', chars=string.ascii_lowercase)
    first_name = FuzzyText()
    last_name = FuzzyText()

    class Meta:
        model = 'checkout.ticket'
