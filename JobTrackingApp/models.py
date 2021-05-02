from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .validations import validate_duration, format_duration

# Create your models here.
class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=60)
    phone_number = models.CharField(blank=True, max_length=30)
    email_address = models.EmailField(blank=True, max_length=30)

    def __str__(self):
        return f"{self.name}"


class ScheduleEvent(models.Model):
    date = models.DateField()
    duration = models.CharField(
        max_length=100,
        validators=[validate_duration],
        blank=True,
    )
    work_order = models.CharField(
        default="-",
        max_length=20,
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    description = models.TextField(max_length=2000, blank=True)

    def __str__(self):
        return f"{self.client.name} --- {self.client.address} --- {self.date}"

    def save(self, *args, **kwargs):
        data = self.duration
        formated_duration = format_duration(data)
        self.duration = formated_duration
        super().save(*args, **kwargs)