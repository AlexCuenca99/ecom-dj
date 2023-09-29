from rest_framework import serializers

from .models import Cart, CartItem
from applications.products.serializers import ProductModelSerializer


class CartItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        exclude = [
            "cart",
        ]


class CartModelSerializer(serializers.ModelSerializer):
    products = CartItemModelSerializer(source="items", many=True)

    class Meta:
        model = Cart
        fields = "__all__"
