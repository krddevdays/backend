from django_enumfield import enum


class ActivityType(enum.Enum):
    WELCOME = 0
    TALK = 1
    COFFEE = 2
    LUNCH = 3
    CLOSE = 4


class SponsorType(enum.Enum):
    SPONSOR = 0
    INFORMATIONAL_PARTNER = 1


class ActivityInterface:
    title = None

    def __str__(self):
        return self.title

    def self_link(self):
        return self.title


class WelcomeActivity(ActivityInterface):
    title = 'Открытие'


class CloseActivity(ActivityInterface):
    title = 'Закрытие'


class CoffeeActivity(ActivityInterface):
    title = 'Кофе-брейк'


class LunchActivity(ActivityInterface):
    title = 'Обед'
