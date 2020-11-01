from django.contrib.postgres.fields import ArrayField
from django.db import models
from enumfields import EnumField

from users.models import User, Company
from .enums import PlacementType, EmploymentType, VacancyStatus, LevelType, PracticeType


class Vacancy(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField()
    skills = ArrayField(models.CharField(max_length=15))
    level = EnumField(LevelType)
    practice = EnumField(PracticeType)
    placement = EnumField(PlacementType)
    address = models.CharField(max_length=200, null=True, blank=True)
    employment = EnumField(EmploymentType)
    link = models.URLField(null=True, blank=True)
    start_cost = models.PositiveIntegerField()
    finish_cost = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    contacts = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    status = EnumField(VacancyStatus, default=VacancyStatus.ACTIVE)

    class Meta:
        verbose_name_plural = 'Vacancies'


class Skill(models.Model):
    name = models.CharField(max_length=20, unique=True)
