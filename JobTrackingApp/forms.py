from django.forms import ModelForm
from django import forms
from .models import Client
from django.core.exceptions import ValidationError
from .validations import fix_phone_number

# from django.utils.translation import gettext_lazy as _


class ClientForm(ModelForm):
    name = forms.CharField(
        error_messages={"invalid": "Client with the same name already exists"}
    )
    name.widget.attrs.update(
        {"placeholder": "required", "autocomplete": "new-password"}
    )
    address = forms.CharField()
    address.widget.attrs.update(
        {"autocomplete": "new-password", "placeholder": "required"}
    )
    phone_number = forms.RegexField(
        regex=r"^(\+?1?)\D*(\d{3})\D*(\d{3})\D*(\d{4})\D*$",
        error_messages={
            "invalid": "Phone number must be entered in the format: '+1-333-666-9999'",
        },
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Example: +1-323-627-8956 (optional)",
                "autocomplete": "new-password",
            }
        ),
    )
    email_address = forms.EmailField(required=False)
    email_address.widget.attrs.update(
        {"placeholder": "optional", "autocomplete": "new-password"}
    )

    class Meta:
        model = Client
        fields = ["name", "address", "phone_number", "email_address"]

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        data = fix_phone_number(data)
        return data


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False)
