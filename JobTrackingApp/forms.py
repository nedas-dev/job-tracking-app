from django.forms import ModelForm
from django import forms
from .models import Client, ScheduleEvent
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


class EventForm(ModelForm):
    date = forms.DateField(
        required=True,
        widget=forms.widgets.DateTimeInput(
            attrs={"type": "date", "placeholder": "mm/dd/yyyy"}
        ),
        error_messages={
            "invalid": "Enter a valid date. 'mm/dd/yyyy'",
        },
    )

    duration = forms.CharField(
        required=False,
        widget=forms.widgets.TextInput(attrs={"placeholder": "example: 2h45min"}),
    )

    class Meta:
        model = ScheduleEvent
        fields = ["date", "duration", "work_order", "client", "description"]

    def __init__(self, user, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["client"].queryset = Client.objects.filter(user=user)


class EventFormEdit(ModelForm):
    class Meta:
        model = ScheduleEvent
        fields = ["date", "duration", "work_order", "client", "description"]


class SortByForm(forms.Form):
    sortby = forms.ChoiceField(
        label="Sort by",
        choices=[
            ("-pk", "Last created (most recent)"),
            ("-date", "Date (Newest to oldest)"),
            ("date", "Date (Oldest to newest)"),
            ("client__name", "Client name (A-Z)"),
            ("-client__name", "Client name (Z-A)"),
        ],
    )

    # def __init__(self, request, *args, **kwargs):
    #     super(SortByForm, self).__init__(self, *args, **kwargs)
