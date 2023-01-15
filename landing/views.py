from django.shortcuts import render
from django.contrib.auth import logout as auth_logout


def index(request):
    return render(request, 'landing/index.html')


def logout(request):
    auth_logout(request)
    return render(request, 'landing/index.html')
