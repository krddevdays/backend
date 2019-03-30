from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.http import JsonResponse


def registration(request):
    pass


def login(request):
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
        auth_login(request, form.get_user())
        return JsonResponse({})
    return JsonResponse(form.errors, status=400)


def logout(request):
    pass
