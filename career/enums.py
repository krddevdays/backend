from enum import Enum


class PlacementType(Enum):
    OFFICE = 'office'
    REMOTE = 'remote'
    BOTH = 'both'


class PracticeType(Enum):
    BACKEND = 'backend'
    FRONTEND = 'frontend'
    MOBILE = 'mobile'
    DESIGN = 'design'
    ADMIN = 'admin'
    QA = 'qa'
    DESKTOP = 'desktop'
    MANAGEMENT = 'management'
    MARKETING = 'marketing'
    ANALYTIC = 'analytics'
    CONTENT = 'content'
    HR = 'hr'
    OTHER = 'other'


class EmploymentType(Enum):
    FULL_TIME = 'full'
    PART_TIME = 'part'
    PROJECT = 'project'
    INTERNSHIP = 'intern'


class VacancyStatus(Enum):
    ACTIVE = 'active'
    ARCHIVED = 'archived'
    DECLINED = 'declined'


class LevelType(Enum):
    INTERN = 'intern'
    JUNIOR = 'junior'
    MIDDLE = 'middle'
    SENIOR = 'senior'
    LEAD = 'lead'
