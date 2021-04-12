from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=256, required=True)

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]
