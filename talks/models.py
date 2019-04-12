from django.db import models

from events.models import Activity


class Speaker(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Talk(models.Model):
    activity = models.OneToOneField(Activity, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    speaker = models.ForeignKey(Speaker, on_delete=models.PROTECT)

    def __str__(self):
        return self.title
