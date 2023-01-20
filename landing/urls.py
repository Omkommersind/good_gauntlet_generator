from django.urls import path

from landing.views import index, register_user

urlpatterns = [
    path('', index, name='index'),
    path('accounts/register', register_user, name="register"),
]
