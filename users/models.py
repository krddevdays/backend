from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    work = models.CharField(max_length=100, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)

    draft_viewer = models.BooleanField(default=False)

    @property
    def can_see_drafts(self) -> bool:
        return self.is_staff or self.draft_viewer

    def __str__(self) -> str:
        return self.email
