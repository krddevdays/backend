from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm


class UserCreationForm(DjangoUserCreationForm):

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            return username.lower()

    class Meta(DjangoUserCreationForm.Meta):
        model = get_user_model()
