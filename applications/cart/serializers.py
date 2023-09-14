from rest_framework import serializers

from .models import Cart


class CartModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
