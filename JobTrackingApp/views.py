from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from . import views


def index(request):
    return render(request, "JobTrackingApp/index.html")
