import json
from functools import wraps

from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views import View

from users.serializers import UserSerializer
from .forms import UserCreationForm, AuthenticationForm


def user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def decode_json(request):
    if request.content_type == 'application/json':
        try:
            return json.loads(request.body)
        except:
            return HttpResponseBadRequest('Cannot decode body.')
    else:
        return request.POST


class UserView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(UserSerializer(request.user).data)

    def patch(self, request, *args, **kwargs):
        serializer = UserSerializer(instance=request.user, data=decode_json(request), partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            return JsonResponse(UserSerializer(instance).data)
        else:
            return JsonResponse(serializer.errors, status=400)


def registration(request):
    form = UserCreationForm(decode_json(request))
    if form.is_valid():
        user = form.save()
        auth_login(request, user)
        return JsonResponse({})
    return JsonResponse(form.errors, status=400)


def login(request):
    form = AuthenticationForm(request, decode_json(request))
    if form.is_valid():
        auth_login(request, form.get_user())
        return JsonResponse({})
    return JsonResponse(form.errors, status=400)


def logout(request):
    auth_logout(request)
    return JsonResponse({})
