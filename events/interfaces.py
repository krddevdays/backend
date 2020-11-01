from typing import Optional

from django_enumfield import enum


class EventStatusType(enum.Enum):
    DRAFT = 0
    PUBLISHED = 1


class ActivityType(enum.Enum):
    WELCOME = 0
    TALK = 1
    COFFEE = 2
    LUNCH = 3
    CLOSE = 4
    DISCUSSION = 5


class PartnerType(enum.Enum):
    SPONSOR = 0
    INFORMATIONAL = 1


class ActivityInterface:
    title: Optional[str] = None

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


class DiscussionActivity(ActivityInterface):
    title = 'Круглый стол'
