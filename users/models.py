from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django_enumfield import enum
from phonenumber_field.modelfields import PhoneNumberField


class CompanyStatus(enum.Enum):
    ACTIVE = 0
    HIDDEN = 1


class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    work = models.CharField(max_length=100, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.email


class Company(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    status = enum.EnumField(CompanyStatus, default=CompanyStatus.ACTIVE)
    address = models.CharField(max_length=200, blank=True, null=True)
    coordinates = ArrayField(models.DecimalField(max_digits=9, decimal_places=6), size=2, null=True, blank=True)
    site = models.URLField(null=True, blank=True)
    phone = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self) -> str:
        return self.title
