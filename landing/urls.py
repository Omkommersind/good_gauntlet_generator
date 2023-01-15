from django.urls import path, include

from landing.views import index, logout

urlpatterns = [
    path('', index, name='index'),
]
