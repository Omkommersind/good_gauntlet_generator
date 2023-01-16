from django.urls import path, include

from landing.views import index, logout_user, register_user

urlpatterns = [
    path('', index, name='index'),
    path('accounts/register', register_user, name="register")
]
