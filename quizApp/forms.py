from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username']


class CustomAuthenticationForm(PopRequestMixin, CreateUpdateAjaxMixin, AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
