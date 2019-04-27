import requests
from django.conf import settings


class QTickets:
    headers = {'Authorization': f'Bearer {settings.QTICKETS_TOKEN}'}
    endpoint = f'{settings.QTICKETS_ENDPOINT}/api/rest/v1/events/'

    @classmethod
    def check_event_exist(cls, external_id: int):
        """ Check qtickets.com system for this event id by calling their API """

        requests.head(f'{cls.endpoint}{external_id}', headers=cls.headers).raise_for_status()
