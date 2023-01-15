from django.urls import path, include


def set_v1_urls(urlpatterns):
    v1_urlpatterns = [
        path('', include('users.versions.v1.urls')),
        path('api/v1/users/', include('users.versions.v1.urls')),
    ]
    urlpatterns.extend(v1_urlpatterns)
