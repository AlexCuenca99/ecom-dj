from rest_framework import serializers

from .models import Cart, CartItem
from applications.products.models import Product


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


# class CartItemModelSerializer(serializers.ModelSerializer):
# products = CartItemModelSerializer(source="items", many=True)

# class Meta:
# model = CartItem
# fields = "__all__"

# def update(self, instance: Cart, validated_data):
# cart_items = validated_data.pop("items")

# for cart_item in cart_items:
# cart_item_product_instance: Product = cart_item.get("product")
# cart_item_quantity = cart_item.get("quantity")

# # Validate if the product stock is greater than the quantity of the
# # cart item
# if cart_item_quantity > cart_item_product_instance.stock:
# raise serializers.ValidationError(
# {
# # "message": f"Stock is not enough for {cart_item_product_instance.name}"
# },
# code="not-enough-product-stock",
# )

# if cart_item_product_instance in instance.products.all():
# raise serializers.ValidationError(
# {
# # "message": f"{cart_item_product_instance.name} is already in cart."
# },
# code="product-already-in-cart",
# )

# return True
