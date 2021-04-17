from django.contrib import admin
from .models import ScheduleEvent, Client

# Register your models here.
admin.site.register(Client)
admin.site.register(ScheduleEvent)