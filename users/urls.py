from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)

from users.views import UserView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='v1-token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='v1-token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='v1-token_verify'),

    path('<str:username>', UserView.as_view(), name='user-detail'),
]
