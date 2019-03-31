from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse

from .forms import UserCreationForm


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
