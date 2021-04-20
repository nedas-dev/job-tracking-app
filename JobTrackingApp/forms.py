from django.forms import ModelForm
from django import forms
from .models import Client


class ClientForm(ModelForm):
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
