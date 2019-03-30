from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse


def registration(request):
    form = UserCreationForm(request, request.POST)
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
    pass
