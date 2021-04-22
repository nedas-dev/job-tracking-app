from django.forms import ModelForm
from django import forms
from .models import Client
from django.core.exceptions import ValidationError

# from django.utils.translation import gettext_lazy as _


class ClientForm(ModelForm):
    name = forms.CharField(
        error_messages={"invalid": "Client with the same name already exists"}
    )
    address = forms.CharField()
    address.widget.attrs.update({"autocomplete": "off"})
    phone_number = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "optional"})
    )
    email_address = forms.EmailField(required=False)
    email_address.widget.attrs.update({"placeholder": "optional"})

    class Meta:
        model = Client
        fields = ["name", "address", "phone_number", "email_address"]