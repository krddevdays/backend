import requests
from django.conf import settings


class ExternalSystemError(Exception):
    pass


def check_qtickets_event(external_id: int):
    """ Check qtickets system for this event id by calling their API """

    headers = {'Authorization': f'Bearer {settings.QTICKETS_TOKEN}'}
    endpoint = f'{settings.QTICKETS_ENDPOINT}/api/rest/v1/events/{external_id}'
    try:
        event_request = requests.head(endpoint, headers=headers)
        event_request.raise_for_status()
    except requests.exceptions.RequestException:
        raise ExternalSystemError(f'Event {external_id} was not found')
