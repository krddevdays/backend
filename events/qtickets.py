import requests
from django.conf import settings

from .exceptions import ExternalSystemError


def check_qtickets_event(external_id: int):
    """ Check qtickets.com system for this event id by calling their API """

    headers = {'Authorization': f'Bearer {settings.QTICKETS_TOKEN}'}
    endpoint = f'{settings.QTICKETS_ENDPOINT}/api/rest/v1/events/{external_id}'
    event_request = requests.head(endpoint, headers=headers)
    if event_request.status_code == 404:
        raise ExternalSystemError(f'Event {external_id} was not found')
    event_request.raise_for_status()
