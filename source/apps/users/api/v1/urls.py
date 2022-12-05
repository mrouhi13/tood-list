from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from apps.users.api.v1.views import RegisterAPIView

app_name = 'users'

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='access-token'),
    path('login/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('register/', RegisterAPIView.as_view(), name='register'),
]
