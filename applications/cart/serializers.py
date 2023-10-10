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


class CartItemBulkCreateSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        cart_id = self.context.get("view").kwargs.get("id")
        cart = Cart.objects.get(id=cart_id)

        valid_new_cart_items = []

        for cart_item in validated_data:
            # Assign cart to item
            cart_item["cart"] = cart
            product: Product = cart_item["product"]
            quantity = cart_item["quantity"]

            if cart_item_product_already_in_cart(product, cart):
                cart_item = CartItem.objects.get(cart=cart, product=product)

                # Reset the quantity of the product
                product.stock += cart_item.quantity
                product.save()

                cart_item.quantity = quantity
                cart_item.save()

                product.stock -= quantity
                product.save()
            else:
                if cart_item_product_stock_is_available(product, quantity):
                    valid_new_cart_items.append(cart_item)
                    product.stock -= quantity
                    product.save()

        cart_item_data = [CartItem(**item) for item in valid_new_cart_items]

        return CartItem.objects.bulk_create(cart_item_data)


def cart_item_product_stock_is_available(product, quantity):
    return product.stock >= quantity


def cart_item_product_already_in_cart(product: Product, cart: Cart) -> bool:
    # If the product is already in the cart
    return CartItem.objects.filter(cart=cart, product=product).exists()


class CartItemCreateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        exclude = [
            "cart",
        ]
        list_serializer_class = CartItemBulkCreateSerializer

    def validate(self, data):
        response = dict()

        quantity = data.get("quantity")
        product: Product = data.get("product")
        cart_id = self.context.get("view").kwargs.get("id")
        cart = Cart.objects.get(id=cart_id)

        """
        Check product existence in the cart
        """

        cart_item = CartItem.objects.filter(cart=cart, product=product)

        if cart_item.exists():
            """
            Check the product availability with restored value
            """
            restored_product_quantity = product.stock + cart_item.first().quantity

            if restored_product_quantity < quantity:
                response[
                    "message"
                ] = f"The new quantity exceed the stock for {product.name}"
                response["code"] = "not-enough-product-stock"
        else:
            """
            Check product availabilty
            """
            if quantity > product.stock:
                response["message"] = f"Stock is not enough for {product.name}"
                response["code"] = "not-enough-product-stock"

        if response:
            raise serializers.ValidationError(response)
        else:
            return data

    def create(self, validated_data):
        cart_id = self.context.get("view").kwargs.get("id")
        cart = Cart.objects.get(id=cart_id)

        quantity = validated_data.get("quantity")
        product: Product = validated_data.get("product")

        cart_item = CartItem.objects.filter(cart=cart, product=product)

        # If the product is already in the cart
        if cart_item.exists():
            cart_item = cart_item.first()

            # Reset the quantity of the product
            product.stock += cart_item.quantity
            product.save()

            cart_item.quantity = quantity
            cart_item.save()

            product.stock -= quantity
            product.save()
        else:
            CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        return cart_item
