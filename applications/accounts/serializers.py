from django.contrib.auth import get_user_model

from djoser.serializers import UserCreatePasswordRetypeSerializer, UserSerializer
from rest_framework import serializers


User = get_user_model()


class UserCreatePasswordRetypeCustomSerializer(UserCreatePasswordRetypeSerializer):
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            "password",
            "email",
        )


class UserCustomSerializer(UserSerializer):
    cart_id = serializers.ReadOnlyField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            ("id",)
            + tuple(User.REQUIRED_FIELDS)
            + (
                "email",
                "is_staff",
                "is_admin",
                "is_superuser",
                "age",
                "photo",
                "cart_id",
            )
        )
