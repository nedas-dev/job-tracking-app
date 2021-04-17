from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from . import views
from .models import Client
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import ClientForm
from django.http import JsonResponse


def index(request):
    return render(request, "JobTrackingApp/index.html")


@login_required
def clients(request):
    clientList = Client.objects.all()
    if request.method == "GET":
        return render(
            request, "JobTrackingApp/clients.html", context={"clientList": clientList}
        )
    elif request.method == "POST":
        form = ClientForm(request)
        if form.is_valid():
            pass


def createClient(request):
    if request.method == "POST":
        return JsonResponse({f"hello": f'{request.POST["hello"]}'})
