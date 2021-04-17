from django.db import models
from django import forms

# Create your models here.
class Client(models.Model):
    name = models.CharField(blank=True, primary_key=True, max_length=100)
    phone_number = models.CharField(blank=True, max_length=100)
    address = models.CharField(max_length=300)
    email_address = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.name}"


class ScheduleEvent(models.Model):
    date = models.DateField()
    work_order = models.CharField(
        default="0",
        max_length=20,
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    unit_number = models.CharField(max_length=8, blank=True)

    def __str__(self):
        return f"{self.client.name} - #{self.unit_number} {self.client.address} (Work Order #{self.work_order})"
