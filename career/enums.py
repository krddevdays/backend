from django_enumfield import enum


class PlacementType(enum.Enum):
    OFFICE = 0
    REMOTE = 1
    BOTH = 2


class EmploymentType(enum.Enum):
    FULL_TIME = 0
    PART_TIME = 1
    PROJECT = 2
