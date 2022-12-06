from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = PasswordField()

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {'username': [
                    'An account with this username is already registered.']})
        return user
