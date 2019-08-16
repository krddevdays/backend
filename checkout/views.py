import hashlib
import hmac
import json

from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

from checkout.models import Ticket, Order
from checkout.serializers import UserTicketsSerializer


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
        return JsonResponse(UserTicketsSerializer(ticket).data)
    else:
        return HttpResponseNotFound()


def user_tickets(request):
    return JsonResponse(UserTicketsSerializer(request.user.tickets.all(), many=True).data, safe=False)


def webhook(request):
    signature = hmac.new(settings.QTICKETS_SECRET.encode(), request.body, hashlib.sha1).hexdigest()
    if signature != request.headers.get('X-Signature'):
        return HttpResponseBadRequest()

    payload = json.loads(request.body)
    Order.add_or_update(payload)
    return HttpResponse()
