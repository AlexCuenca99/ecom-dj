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


class CartItemCreateModelSerializer(serializers.Serializer):
    items = CartItemModelSerializer(many=True)

    def to_representation(self, instance):
        print("\n\nINSTANCE->", instance)
        cart_item_serializer = CartItemModelSerializer(instance, many=True)
        return cart_item_serializer.data

    def create(self, validated_data):
        cart_id = self.context.get("view").kwargs.get("id")
        cart = Cart.objects.get(id=cart_id)

        items = validated_data.get("items")

        for item in items:
            quantity = item.get("quantity")
            product: Product = item.get("product")

            # If the product is already in the cart
            if CartItem.objects.filter(cart=cart, product=product).exists():
                cart_item = CartItem.objects.get(cart=cart, product=product)

                # Reset the quantity of the product
                product.stock += cart_item.quantity
                product.save()

                # Validate quantity with stock
                if quantity > product.stock:
                    raise serializers.ValidationError(
                        {"message": f"Stock is not enough for {product.name}"},
                        code="not-enough-product-stock",
                    )
                else:
                    cart_item.quantity = quantity
                    cart_item.save()
            else:
                # Validate quantity with stock
                if quantity > product.stock:
                    raise serializers.ValidationError(
                        {"message": f"Stock is not enough for {product.name}"},
                        code="not-enough-product-stock",
                    )
                else:
                    CartItem.objects.create(
                        cart=cart, product=product, quantity=quantity
                    )

        return CartItem.objects.filter(cart=cart)


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
