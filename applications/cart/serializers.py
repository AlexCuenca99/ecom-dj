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

        validated_items = list()
        validation_error = dict()

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

                if cart_item_product_stock_is_available(product, quantity):
                    cart_item.quantity = quantity
                    cart_item.save()
                else:
                    validation_error[
                        "message"
                    ] = f"Stock is not enough for {product.name}"
                    validation_error["code"] = "not-enough-product-stock"
            else:
                if cart_item_product_stock_is_available(product, quantity):
                    validated_items.append(cart_item)
                else:
                    validation_error[
                        "message"
                    ] = f"Stock is not enough for {product.name}"
                    validation_error["code"] = "not-enough-product-stock"

        if validation_error:
            raise serializers.ValidationError(validation_error)

        cart_item_data = [CartItem(**item) for item in validated_items]

        # return CartItem.objects.bulk_create(cart_item_data)


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
        """
        Check product availabilty
        """
        print(data)

    def create(self, validated_data):
        cart_id = self.context.get("view").kwargs.get("id")
        cart = Cart.objects.get(id=cart_id)

        quantity = validated_data.get("quantity")
        product: Product = validated_data.get("product")

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
                CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        return cart_item
