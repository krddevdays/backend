from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm, AuthenticationForm as DjangoAuthenticationForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode

UserModel = get_user_model()


class UserCreationForm(DjangoUserCreationForm):
    email = forms.CharField(strip=False)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            return username.lower()

    class Meta(DjangoUserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email', 'first_name', 'last_name')


class AuthenticationForm(DjangoAuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            return username.lower()


class PasswordSetForm(forms.Form):
    uid = forms.CharField()
    token = forms.CharField()
    password = forms.CharField(strip=False)
    user = None

    def clean(self):
        try:
            uid = urlsafe_base64_decode(self.cleaned_data['uid']).decode()
            self.user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            raise ValidationError('Malformed uid')

        if not default_token_generator.check_token(self.user, self.cleaned_data['token']):
            raise ValidationError('Malformed token')

    def save(self):
        password = self.cleaned_data["password"]
        self.user.set_password(password)
        self.user.save()
        return self.user
