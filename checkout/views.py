import hashlib
import hmac
import json

from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

from checkout.models import Ticket, Order


def link_user_qtickets(request):
    if request.user.is_anonymous:
        return HttpResponseForbidden('Authorization required.')

    try:
        data = json.loads(request.body)
    except:
        return HttpResponseBadRequest('Cannot decode body.')

    ticket = get_object_or_404(Ticket, qticket_id=data.get('id'))
    if ticket and ticket.email == data.get('email'):
        ticket.user = request.user
        ticket.save()
        return JsonResponse({})
    else:
        return HttpResponseNotFound()


def webhook(request):
    if hmac.new(settings.QTICKET_SECRET, request.body, hashlib.sha1).hexdigest() != request.headers.get('X-Signature'):
        return HttpResponseBadRequest()

    event = request.headers.get('X-Event-Type')
    payload = json.loads(request.body)
    if event == 'created':
        Order.add(payload)
    else:
        client = payload['client']
        order = get_object_or_404(Order, qticket_id=payload['id'])
        order.response = payload
        order.email = client['email']
        order.first_name = client['details']['name']
        order.last_name = client['details']['surname']
        order.save()
        to_remove = set(order.tickets.values_list('qticket_id'))
        for ticket in payload['baskets']:
            to_remove.remove(ticket['id'])
            try:
                original = Ticket.objects.get(qticket_id=ticket['id'])
            except Ticket.DoesNotExist:
                original = Ticket(qticket_id=ticket['id'], order=order)
            if original.email != ticket['client_email']:
                original.email = ticket['client_email']
                original.user = None
            original.first_name = ticket['client_name']
            original.last_name = ticket['client_surname']
            original.save()
        Ticket.objects.filter(qticket_id__in=to_remove).delete()

    return HttpResponse()
