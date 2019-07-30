import json
from functools import wraps

from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views import View

from users.serializers import UserSerializer
from .forms import UserCreationForm


def user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)
    return _wrapped_view


class UserView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(UserSerializer(request.user).data)

    def patch(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except:
            return HttpResponseBadRequest('Cannot decode body.')

        serializer = UserSerializer(instance=request.user, data=data)
        if serializer.is_valid():
            instance = serializer.save()
            return JsonResponse(UserSerializer(instance).data)
        else:
            return JsonResponse(serializer.errors, status=400)


def registration(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        auth_login(request, user)
        return JsonResponse({})
    return JsonResponse(form.errors, status=400)


def login(request):
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
        auth_login(request, form.get_user())
        return JsonResponse({})
    return JsonResponse(form.errors, status=400)


def logout(request):
    auth_logout(request)
    return JsonResponse({})
