from django_enumfield import enum


class ActivityType(enum.Enum):
    WELCOME = 0
    TALK = 1
    COFFEE = 2
    LUNCH = 3


class ActivityInterface:
    title = None

    def __str__(self):
        return self.title

    def self_link(self):
        return self.title


class WelcomeActivity(ActivityInterface):
    title = 'Открытие'


class CoffeeActivity(ActivityInterface):
    title = 'Кофе-брейк'


class LunchActivity(ActivityInterface):
    title = 'Обед'
