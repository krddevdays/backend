import json
from functools import wraps
from json import JSONDecodeError

from django.conf import settings
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import PasswordResetForm
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views import View
from rest_framework import mixins, viewsets, permissions
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from .serializers import UserSerializer, CompanySerializer
from .forms import UserCreationForm, AuthenticationForm, PasswordSetForm
from .models import Company, CompanyStatus


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
        except JSONDecodeError:
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


def reset_password(request):
    form = PasswordResetForm(decode_json(request))
    if form.is_valid():
        form.save(use_https=True, domain_override=settings.ALLOWED_HOSTS[0], from_email=settings.DEFAULT_FROM_EMAIL,
                  subject_template_name='reset_password/subject.txt', email_template_name='reset_password/body.html')
        return JsonResponse({})
    return JsonResponse(form.errors, status=400)


def set_password(request):
    form = PasswordSetForm(decode_json(request))
    if form.is_valid():
        user = form.save()
        auth_login(request, user)
        return JsonResponse({})
    return JsonResponse(form.errors, status=400)


class CompanyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CompanyViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                     mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Company.objects.filter(status=CompanyStatus.ACTIVE).all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = CompanyPagination

    def perform_create(self, serializer: CompanySerializer):
        serializer.save(owner=self.request.user)
