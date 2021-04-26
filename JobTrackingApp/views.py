from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseNotFound
from . import views
from .forms import ClientForm, SearchForm
from .models import Client
from django.core.exceptions import ValidationError
from .validations import fix_phone_number
from django.core.paginator import Paginator
from django.contrib import messages


def index(request):
    return render(request, "JobTrackingApp/index.html")


@login_required
def clients(request):
    clientList = Client.objects.filter(user=request.user).order_by("name")
    if request.method == "GET":
        form = ClientForm()
        searchForm = SearchForm(request.GET)
        if searchForm.is_valid():
            data = searchForm.cleaned_data
            query = data["query"]
            if query:
                clientList = clientList.filter(name__icontains=query)

    elif request.method == "POST":
        form = ClientForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            if not clientList.filter(name=data["name"]).exists():
                phone_number = fix_phone_number(data["phone_number"])
                client = Client(
                    user=request.user,
                    address=data["address"],
                    name=data["name"],
                    phone_number=phone_number,
                    email_address=data["email_address"],
                )
                client.save()
                messages.success(request, "You have successfully created a new client!")
                return redirect(reverse("clients"))
            else:
                form.add_error("name", "Client with the same name already exists")

    page_number = request.GET.get("page", 1)
    paginator = Paginator(clientList, 15)
    pageList = paginator.get_page(page_number)

    context = {
        "paginator": paginator,
        "page_obj": pageList,
        "form": form,
        "searchForm": searchForm,
        "is_paginated": True,
        "search": query,
    }

    return render(
        request,
        "JobTrackingApp/clients.html",
        context,
    )


@login_required
def clientDetailView(request, pk):
    clientObj = Client.objects.filter(user=request.user).filter(pk=pk)
    exists = clientObj.exists()

    if exists and request.method == "GET":
        form = ClientForm(instance=clientObj[0])
        context = {"form": form, "pk": clientObj[0].pk}
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
            messages.success(request, f"You have successfully updated {data['name']}!")
            return redirect(reverse("clients"))
        else:
            return render(
                request,
                "JobTrackingApp/clientDetailView.html",
                {"form": form},
            )
    else:
        return HttpResponseNotFound("404 Page not found")


@login_required
def clientDeleteView(request, pk):
    clientObj = Client.objects.filter(user=request.user).filter(pk=pk)

    client_exists = clientObj.exists()
    if client_exists:
        context = {"client_obj": clientObj[0]}
    else:
        return HttpResponseNotFound("Something went wrong")

    if (
        request.method == "POST"
        and client_exists
        and request.POST.get("action") == "Yes"
    ):
        name = clientObj[0].name
        clientObj[0].delete()
        messages.success(request, f"You have successfully deleted {name}!")
        return redirect(reverse("clients"))
    elif (
        request.method == "POST"
        and client_exists
        and request.POST.get("action") == "No"
    ):
        return redirect(reverse("client-detail", args=[pk]))

    return render(request, "JobTrackingApp/clientDeleteView.html", context=context)
