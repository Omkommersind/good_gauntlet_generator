import debug_toolbar
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from good_gauntlet_generator import settings

urlpatterns = [
                  path('__debug__/', include(debug_toolbar.urls)),
                  path('admin/', admin.site.urls),
                  path('', include('landing.urls')),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('users/', include('users.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

