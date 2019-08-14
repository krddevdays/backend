import json

from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404

from checkout.models import Ticket


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
