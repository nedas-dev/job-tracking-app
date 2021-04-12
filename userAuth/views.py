from django.shortcuts import render
from django.http import HttpResponse
from . import views
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, reverse


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = data["email"]
            password = data["password1"]
            user = User.objects.create_user(
                username=email, email=email, password=password
            )
            user.save()
            return redirect(reverse("login"))
    else:
        form = SignUpForm()

    return render(request, "userAuth/register.html", {"form": form})
