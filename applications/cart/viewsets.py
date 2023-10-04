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
from .serializers import CartModelSerializer, CartItemModelSerializer


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
    serializer_class = CartItemModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return self.request.user.cart.items.all()

    def get_instance(self):
        return self.request.user.cart

    @swagger_auto_schema(
        request_body=CartItemModelSerializer(many=True),
        responses={200: CartModelSerializer()},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # TODO: Create a method to get my cart items
