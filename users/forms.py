from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm, AuthenticationForm as DjangoAuthenticationForm


class UserCreationForm(DjangoUserCreationForm):
    email = forms.CharField(strip=False)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            return username.lower()

    class Meta(DjangoUserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')


class AuthenticationForm(DjangoAuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            return username.lower()
