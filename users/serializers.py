from typing import Dict

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import User


class UserSerializer(serializers.ModelSerializer):
    instance: User
    confirm_password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "password", "confirm_password", "is_active"]
        extra_kwargs = {
            "password": {"write_only": True},
            "is_active": {"read_only": True},
        }

    def validate(self, data: Dict):
        confirm_password = data.pop("confirm_password", None)
        if not self.instance:
            if data["password"] != confirm_password:
                raise ValidationError(_("Passwords did not match"))

            user = User(**data)
            validate_password(data["password"], user)

        return data

    def create(self, validated_data: Dict):
        user = User.objects.create_user(**validated_data)
        return user
