import requests
from django.conf import settings


def check_qtickets_event(external_id: int):
    """ Check qtickets.com system for this event id by calling their API """

    headers = {'Authorization': f'Bearer {settings.QTICKETS_TOKEN}'}
    endpoint = f'{settings.QTICKETS_ENDPOINT}/api/rest/v1/events/{external_id}'
    requests.head(endpoint, headers=headers).raise_for_status()
