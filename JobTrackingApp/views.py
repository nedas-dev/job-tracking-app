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
    clientList = Client.objects.filter(user=request.user)
    if request.method == "GET":
        form = ClientForm()
        context = {"clientList": clientList, "form": form}
        return render(
            request,
            "JobTrackingApp/clients.html",
            context,
        )
    elif request.method == "POST":
        form = ClientForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            if not clientList.filter(name=data["name"]).exists():
                client = Client(
                    user=request.user,
                    address=data["address"],
                    name=data["name"],
                    phone_number=data["phone_number"],
                    email_address=data["email_address"],
                )
                client.save()
                data["is_valid"] = True
                data["message"] = "Client was successfully created"
            else:
                data = {
                    "is_valid": False,
                    "message": "Client already exists",
                }
        else:
            data = {
                "is_valid": False,
                "message": "Error: Client was NOT created",
            }

    return JsonResponse(data)