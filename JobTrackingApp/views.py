from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseNotFound
from . import views
from .forms import ClientForm, SearchForm, EventForm, EventFormEdit
from .models import Client, ScheduleEvent
from django.core.exceptions import ValidationError
from .validations import fix_phone_number
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q


@login_required
def index(request):
    context = {}
    query = ""
    eventForm = EventForm(user=request.user)

    events = ScheduleEvent.objects.filter(client__user=request.user).order_by("-pk")

    searchForm = SearchForm(request.GET)
    if request.method == "GET":
        if searchForm.is_valid() and searchForm.cleaned_data["query"]:
            data = searchForm.cleaned_data
            query = data["query"]
            if query:
                events = events.filter(
                    Q(client__name__icontains=query)
                    | Q(description__icontains=query)
                    | Q(client__address__icontains=query)
                    | Q(work_order__icontains=query)
                )
    elif request.method == "POST":
        eventForm = EventForm(request.user, request.POST)
        if eventForm.is_valid():
            eventForm.save()
            messages.success(request, "You have successfully created an event!")
            return redirect(reverse("index"))
        else:
            eventForm = EventForm(request.user, request.POST)

    page_number = request.GET.get("page", 1)
    paginator = Paginator(events, 12)
    pageList = paginator.get_page(page_number)

    context["searchForm"] = searchForm
    context["search"] = query
    context["eventForm"] = eventForm
    context["paginator"] = paginator
    context["is_paginated"] = True
    context["page_obj"] = pageList

    return render(request, "JobTrackingApp/index.html", context)


@login_required
def editEvent(request, pk):
    context = {}
    if request.method == "GET":
        instance = get_object_or_404(ScheduleEvent, pk=pk)
        eventForm = EventFormEdit(instance=instance)
        context["eventForm"] = eventForm
    elif request.method == "POST":
        instance = get_object_or_404(ScheduleEvent, pk=pk)
        eventForm = EventFormEdit(request.POST, instance=instance)
        if eventForm.is_valid():
            eventForm.save()
            messages.success(request, "You successfully updated an event!")
            return redirect(reverse("index"))
        else:
            context["eventForm"] = eventForm

    return render(request, "JobTrackingApp/eventEditView.html", context)


@login_required
def clients(request):
    query = ""
    clientList = Client.objects.filter(user=request.user).order_by("name")
    searchForm = SearchForm(request.GET)
    if request.method == "GET":
        form = ClientForm()
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
    paginator = Paginator(clientList, 10)
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
    context = {}
    context["pk"] = pk
    if exists and request.method == "GET":
        form = ClientForm(instance=clientObj[0])
        context["form"] = form
        return render(
            request,
            "JobTrackingApp/clientDetailView.html",
            context,
        )
    elif exists and request.method == "POST":
        form = ClientForm(request.POST, instance=clientObj[0])
        context["form"] = form
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
                    context,
                )
            form.save()
            messages.success(
                request,
                f"You have successfully updated {data['name']}!",
            )
            return redirect(reverse("clients"))
        else:
            return render(
                request,
                "JobTrackingApp/clientDetailView.html",
                context=context,
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
