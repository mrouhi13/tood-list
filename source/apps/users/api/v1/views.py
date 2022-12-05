from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.decorators import method_decorator
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.api.v1.serializers import RegisterSerializer

User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    """
    Register a new user by given email or mobile and password.
    """
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    @method_decorator(transaction.atomic)
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)

        user.save()

        return Response(
            {'refresh': str(token), 'access': str(token.access_token)},
            status=status.HTTP_201_CREATED)
