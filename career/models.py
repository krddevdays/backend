from django.contrib.postgres.fields import ArrayField
from django.db import models
from django_enumfield import enum

from users.models import User
from .enums import PlacementType, EmploymentType, VacancyStatus


class Vacancy(models.Model):
    company = models.CharField(max_length=120)
    title = models.CharField(max_length=120)
    description = models.TextField()
    technologies = ArrayField(models.CharField(max_length=15))
    placement = enum.EnumField(PlacementType)
    address = models.CharField(max_length=200, null=True)
    employment = enum.EnumField(EmploymentType)
    link = models.URLField(null=True)
    start_cost = models.PositiveIntegerField()
    finish_cost = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    status = enum.EnumField(VacancyStatus, default=VacancyStatus.ACTIVE)

    class Meta:
        verbose_name_plural = 'Vacancies'


class Technology(models.Model):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name_plural = 'technologies'
