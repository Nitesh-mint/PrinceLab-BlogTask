from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)  # default django form
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful signup
            return redirect("blogs/post_list_htmx.html")  # Redirect to a home page or any other page
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def profile(request):
    return render(request, "registration/profile.html")


def home(request):
    return render(request, "home.html")


def logged_out(request):
    return render(request, "registration/logged_out.html")
