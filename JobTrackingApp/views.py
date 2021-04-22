from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseNotFound
from . import views
from .forms import ClientForm
from .models import Client
from django.core.exceptions import ValidationError


def index(request):
    return render(request, "JobTrackingApp/index.html")


@login_required
def clients(request):
    clientList = Client.objects.filter(user=request.user).order_by("-pk")
    if request.method == "GET":
        form = ClientForm()
        context = {
            "clientList": clientList,
            "form": form,
        }
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
                form.add_error("name", "Client with the same name already exists")

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


@login_required
def clientDetailView(request, pk):
    clientObj = Client.objects.filter(user=request.user).filter(pk=pk)
    exists = clientObj.exists()
    if exists and request.method == "GET":
        form = ClientForm(instance=clientObj[0])
        context = {"form": form}
        return render(
            request,
            "JobTrackingApp/clientDetailView.html",
            context,
        )
    elif exists and request.method == "POST":
        form = ClientForm(request.POST, instance=clientObj[0])
        if form.is_valid():
            data = form.cleaned_data
            exists = (
                Client.objects.filter(user=request.user)
                .filter(name=data["name"])
                .exclude(pk=pk)
                .exists()
            )
            if exists:
                form.add_error("name", "A client with the same name already exists.")
                return render(
                    request,
                    "JobTrackingApp/clientDetailView.html",
                    {"form": form},
                )
            form.save()
            return redirect(reverse("clients"))
        else:
            return render(
                request,
                "JobTrackingApp/clientDetailView.html",
                {"form": form},
            )
    else:
        return HttpResponseNotFound("404 Page not found")
