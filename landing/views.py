from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from landing.forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages


def index(request):
    return render(request, 'landing/index.html')


def logout_user(request):
    auth_logout(request)
    return redirect('index')


def register_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('index')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="registration/register.html", context={"register_form": form})
