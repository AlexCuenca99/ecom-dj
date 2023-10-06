from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    SAFE_METHODS,
)
from drf_yasg.utils import swagger_auto_schema

from .models import Cart, CartItem
from .serializers import (
    CartModelSerializer,
    CartItemModelSerializer,
    CartItemCreateModelSerializer,
)


class CartModelViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartModelSerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]

    def get_instance(self):
        return self.request.user.cart

    @action(
        detail=False,
        methods=["GET"],
        name="My cart",
        url_path="my-cart",
        url_name="my-cart",
        pagination_class=None,
    )
    def my_cart(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)


class CartItemModelViewSet(ModelViewSet):
    serializer_class = CartItemCreateModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_cart_instance(self):
        cart_id = self.kwargs.get("id", None)

        if cart_id is None:
            return None

        return Cart.objects.get(id=cart_id)

    def get_my_cart_instance(self):
        return self.request.user.cart

    def get_queryset(self):
        cart = self.get_cart_instance()

        if cart is None:
            return CartItem.objects.none()

        return cart.items.all()

    @swagger_auto_schema(
        request_body=CartItemCreateModelSerializer(many=True),
        responses={200: CartModelSerializer(many=False)},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # TODO: Create a method to get my cart items
