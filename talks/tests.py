from django.apps import apps
from django.test import TestCase
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework.reverse import reverse

from events.factories import ActivityFactory, EventFactory
from events.interfaces import ActivityType
from events.models import Event
from talks.apps import TalksConfig
from talks.factories import TalkFactory, SpeakerFactory, DiscussionFactory
from talks.models import Talk, Discussion
from users.factories import UserFactory
from users.models import User


class TalkTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.talk: Talk = TalkFactory()

    def _check_talk(self, data: dict, talk: Talk):
        self.assertEqual(data['title'], talk.title)
        self.assertEqual(data['description'], talk.description)
        self.assertEqual(data['video'], talk.video)
        self.assertEqual(data['poster_image'], talk.poster_image)
        self.assertEqual(data['presentation_offline'], talk.presentation_offline)
        self.assertEqual(data['speaker']['first_name'], talk.speaker.first_name)
        self.assertEqual(data['speaker']['last_name'], talk.speaker.last_name)
        self.assertEqual(data['speaker']['avatar'], talk.speaker.avatar)
        self.assertEqual(data['speaker']['work'], talk.speaker.work)
        self.assertEqual(data['speaker']['position'], talk.speaker.position)

    def test_apps(self):
        self.assertEqual(TalksConfig.name, 'talks')
        self.assertEqual(apps.get_app_config('talks').name, 'talks')

    def test_talks_list(self):
        response = self.client.get(reverse('talk-list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self._check_talk(data[0], self.talk)

        TalkFactory()
        response = self.client.get(reverse('talk-list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)

    def test_talk(self):
        response = self.client.get(reverse('talk-detail', args=(self.talk.id,)))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self._check_talk(data, self.talk)

    def test_talk_filter(self):
        event = EventFactory()
        talk = TalkFactory(event=event)
        response = self.client.get(reverse('talk-list'), data={'event_id': event.id})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['event_id'], talk.event_id)

    def test_str(self):
        speaker = SpeakerFactory(first_name='Марк', last_name='Ланговой')
        self.assertEqual(str(speaker), 'Марк Ланговой')

    def test_activity_interface(self):
        activity = ActivityFactory(type=ActivityType.TALK)
        talk: Talk = TalkFactory(activity=activity)
        self.assertEqual(talk.self_link(), f'<a href="/admin/talks/talk/{talk.id}/change/">{talk.title}</a>')

        response = self.client.get(reverse('event-activities', args=(activity.event.id,)))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        obj = data[0]
        self.assertEqual(obj['type'], 'TALK')
        self._check_talk(obj['thing'], talk)


class DiscussionTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.event: Event = EventFactory(discussion_start=timezone.now())
        cls.user: User = UserFactory()

    def test_activity_interface(self):
        activity = ActivityFactory(type=ActivityType.DISCUSSION)
        discussion: Discussion = DiscussionFactory(activity=activity)
        self.assertEqual(discussion.self_link(), f'<a href="/admin/talks/discussion/{discussion.id}/change/">{discussion.title}</a>')

        response = self.client.get(reverse('event-activities', args=(activity.event.id,)))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        obj = data[0]
        self.assertEqual(obj['type'], 'DISCUSSION')

    def test_list(self):
        discussion = DiscussionFactory(event=self.event, author=self.user)
        response = self.client.get(reverse('discussion-list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        obj = data[0]
        self.assertEqual(obj['event_id'], self.event.id)
        self.assertEqual(obj['title'], discussion.title)
        self.assertEqual(obj['description'], discussion.description)
        self.assertEqual(obj['votes_count'], 0)
        self.assertEqual(obj['is_author'], False)

    def test_create(self):
        data = {
            'event_id': self.event.id,
            'title': get_random_string(),
            'description': get_random_string()
        }
        response = self.client.post(reverse('discussion-list'), data=data)
        self.assertEqual(response.status_code, 403)  # https://github.com/encode/django-rest-framework/issues/5968

        credentials = {'username': self.user.username, 'password': self.user.original_password}
        response = self.client.post(reverse('login'), credentials)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('discussion-list'), data=data)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['is_author'], True)

        bad_data = {
            'title': get_random_string(),
            'description': get_random_string()
        }
        response = self.client.post(reverse('discussion-list'), data=bad_data)
        self.assertEqual(response.status_code, 400)
        errors = response.json()
        self.assertIn('event_id', errors)

    def test_start_finish_dates(self):
        event = EventFactory()
        data = {
            'event_id': event.id,
            'title': get_random_string(),
            'description': get_random_string()
        }
        credentials = {'username': self.user.username, 'password': self.user.original_password}
        response = self.client.post(reverse('login'), credentials)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('discussion-list'), data=data)
        self.assertEqual(response.status_code, 400)

        event.discussion_start = timezone.now()
        event.discussion_finish = timezone.now()
        event.save()
        response = self.client.post(reverse('discussion-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_vote(self):
        discussion = DiscussionFactory(event=self.event)
        response = self.client.post(reverse('discussion-detail', args=(discussion.id,)))
        self.assertEqual(response.status_code, 403)  # https://github.com/encode/django-rest-framework/issues/5968

        credentials = {'username': self.user.username, 'password': self.user.original_password}
        self.client.post(reverse('login'), credentials)

        response = self.client.post(reverse('discussion-vote', args=(discussion.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(discussion.votes.count(), 1)
        response = self.client.get(reverse('discussion-detail', args=(discussion.id,)))
        data = response.json()
        self.assertEqual(data['my_vote'], True)

        response = self.client.post(reverse('discussion-vote', args=(discussion.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(discussion.votes.count(), 0)
        response = self.client.get(reverse('discussion-detail', args=(discussion.id,)))
        data = response.json()
        self.assertEqual(data['my_vote'], False)

    def test_talk_filter(self):
        event = EventFactory()
        discussion = DiscussionFactory(event=event)
        response = self.client.get(reverse('discussion-list'), data={'event_id': event.id})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['event_id'], discussion.event_id)
