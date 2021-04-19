from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse, HttpResponseNotFound
from . import views
from .forms import ClientForm
from .models import Client


def index(request):
    return render(request, "JobTrackingApp/index.html")


@login_required
def clientDetailView(request, pk):
    client_detail = Client.objects.filter(user=request.user).filter(pk=pk)
    if client_detail.exists():
        form = ClientForm(instance=client_detail[0])
        context = {"form": form}
        return render(request, "JobTrackingApp/clientDetailView.html", context)
    else:
        return HttpResponseNotFound("404 Page not found")


@login_required
def clients(request):
    clientList = Client.objects.filter(user=request.user).order_by("-pk")
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