from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm


class UserCreationForm(DjangoUserCreationForm):
    email = forms.CharField(strip=False)

    class Meta(DjangoUserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email')
