from django.db import models
from django.urls import reverse

from events.interfaces import ActivityInterface
from events.models import Activity, Event
from users.models import User


class Speaker(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    avatar = models.URLField(blank=True, null=True)
    work = models.CharField(max_length=100, null=True, blank=True)
    position = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Talk(ActivityInterface, models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT, null=True, blank=True)
    activity = models.OneToOneField(Activity, on_delete=models.PROTECT, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    poster_image = models.URLField(null=True, blank=True)
    speaker = models.ForeignKey(Speaker, on_delete=models.PROTECT)
    presentation_online = models.URLField(null=True, blank=True)
    presentation_offline = models.URLField(null=True, blank=True)
    video = models.URLField(null=True, blank=True)

    def self_link(self):
        return f"<a href=\"{reverse('admin:talks_talk_change', args=(self.id,))}\">{self.title}</a>"


class Discussion(ActivityInterface, models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT, null=True, blank=True)
    activity = models.OneToOneField(Activity, on_delete=models.PROTECT, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    speaker = models.ForeignKey(User, on_delete=models.PROTECT, related_name='discussions')
    votes = models.ManyToManyField(User, blank=True)

    def self_link(self):
        return f"<a href=\"{reverse('admin:talks_discussion_change', args=(self.id,))}\">{self.title}</a>"
